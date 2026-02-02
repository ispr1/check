"""
PDF Metadata Analyzer.

Checks:
- Creator software (Photoshop = suspicious)
- Creation/modification dates
- Producer info
"""

import logging
from typing import Optional
from io import BytesIO
from datetime import datetime

from ..contracts import LayerResult
from ..rules import SUSPICIOUS_CREATORS, TRUSTED_CREATORS, DEFAULT_SCORES

logger = logging.getLogger(__name__)


class MetadataAnalyzer:
    """
    Analyze PDF metadata for suspicious patterns.
    
    Red flags:
    - Created with image editing software
    - Modified before creation date
    - Missing expected metadata
    """
    
    def analyze(self, file_bytes: bytes) -> LayerResult:
        """
        Analyze PDF metadata.
        
        Returns LayerResult with score and flags.
        """
        try:
            import pikepdf
        except ImportError:
            logger.warning("pikepdf not installed, skipping metadata analysis")
            return LayerResult(
                name="metadata",
                score=DEFAULT_SCORES["clean"],
                flags=["ANALYZER_NOT_AVAILABLE"],
            )
        
        flags = []
        score = DEFAULT_SCORES["clean"]
        details = {}
        
        try:
            pdf = pikepdf.open(BytesIO(file_bytes))
            docinfo = pdf.docinfo
            
            # Extract metadata
            creator = self._get_string(docinfo, '/Creator')
            producer = self._get_string(docinfo, '/Producer')
            creation_date = self._get_string(docinfo, '/CreationDate')
            mod_date = self._get_string(docinfo, '/ModDate')
            
            details = {
                "creator": creator,
                "producer": producer,
                "creation_date": creation_date,
                "mod_date": mod_date,
            }
            
            # Check 1: Creator software
            if creator:
                creator_lower = creator.lower()
                
                # Check for suspicious creators (image editors)
                for suspicious in SUSPICIOUS_CREATORS:
                    if suspicious in creator_lower:
                        flags.append(f"CREATED_WITH_IMAGE_EDITOR: {creator}")
                        score = min(score, DEFAULT_SCORES["major_issue"])
                        break
                
                # Bonus for trusted creators
                for trusted in TRUSTED_CREATORS:
                    if trusted in creator_lower:
                        details["trusted_creator"] = True
                        break
            
            # Check 2: Date consistency
            if creation_date and mod_date:
                try:
                    created = self._parse_pdf_date(creation_date)
                    modified = self._parse_pdf_date(mod_date)
                    
                    if created and modified:
                        if modified < created:
                            flags.append("MODIFIED_BEFORE_CREATED")
                            score = min(score, DEFAULT_SCORES["moderate_issue"])
                        
                        # Very old creation with recent modification
                        age_days = (datetime.now() - created).days
                        mod_age_days = (datetime.now() - modified).days
                        
                        if age_days > 365 * 10 and mod_age_days < 30:
                            flags.append("OLD_DOCUMENT_RECENTLY_MODIFIED")
                            score = min(score, DEFAULT_SCORES["minor_issue"])
                
                except Exception as e:
                    logger.debug(f"Date parsing error: {e}")
            
            # Check 3: Missing metadata (minor flag)
            if not creator and not producer:
                flags.append("NO_CREATOR_INFO")
                score = min(score, DEFAULT_SCORES["minor_issue"])
            
            pdf.close()
            
        except Exception as e:
            logger.warning(f"Metadata analysis failed: {e}")
            return LayerResult(
                name="metadata",
                score=DEFAULT_SCORES["minor_issue"],
                flags=["ANALYSIS_ERROR"],
                details={"error": str(e)},
            )
        
        return LayerResult(
            name="metadata",
            score=score,
            flags=flags,
            details=details,
        )
    
    def _get_string(self, docinfo, key: str) -> Optional[str]:
        """Safely extract string from docinfo."""
        try:
            if key in docinfo:
                return str(docinfo[key])
        except:
            pass
        return None
    
    def _parse_pdf_date(self, date_str: str) -> Optional[datetime]:
        """Parse PDF date format (D:YYYYMMDDHHmmSS)."""
        try:
            # Remove 'D:' prefix if present
            if date_str.startswith('D:'):
                date_str = date_str[2:]
            
            # Take first 14 characters (YYYYMMDDHHmmSS)
            date_str = date_str[:14]
            
            return datetime.strptime(date_str, '%Y%m%d%H%M%S')
        except:
            return None
