"""
Text Format Analyzer.

Validates:
- PAN format (not existence)
- Aadhaar format (not existence)
- Date consistency
- Basic sanity checks
"""

import re
import logging
from io import BytesIO
from typing import List, Tuple

from ..contracts import LayerResult
from ..rules import (
    VALID_PAN_ENTITY_TYPES,
    AADHAAR_PATTERN,
    DATE_PATTERNS,
    DEFAULT_SCORES,
)

logger = logging.getLogger(__name__)


class TextAnalyzer:
    """
    Analyze document text for format validation.
    
    NOTE: This ONLY validates format, NOT existence.
    Existence checking is done by Surepass in Phase 2.
    """
    
    def analyze(self, file_bytes: bytes, doc_type: str = "other") -> LayerResult:
        """
        Analyze text content of PDF.
        
        Returns LayerResult with score and flags.
        """
        try:
            import pdfplumber
        except ImportError:
            logger.warning("pdfplumber not installed, skipping text analysis")
            return LayerResult(
                name="text",
                score=DEFAULT_SCORES["clean"],
                flags=["ANALYZER_NOT_AVAILABLE"],
            )
        
        flags = []
        score = DEFAULT_SCORES["clean"]
        details = {}
        
        try:
            with pdfplumber.open(BytesIO(file_bytes)) as pdf:
                full_text = ""
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    full_text += page_text + "\n"
                
                details["char_count"] = len(full_text)
                details["page_count"] = len(pdf.pages)
            
            # Check 1: PAN format validation
            pan_flags, pan_valid_count = self._check_pan_format(full_text)
            flags.extend(pan_flags)
            details["pan_found"] = pan_valid_count
            
            # Check 2: Aadhaar format validation  
            aadhaar_flags, aadhaar_valid_count = self._check_aadhaar_format(full_text)
            flags.extend(aadhaar_flags)
            details["aadhaar_found"] = aadhaar_valid_count
            
            # Check 3: Date format consistency
            date_flags = self._check_date_consistency(full_text)
            flags.extend(date_flags)
            
            # Check 4: Empty or too short
            if len(full_text.strip()) < 50:
                flags.append("MINIMAL_TEXT_CONTENT")
                score = min(score, DEFAULT_SCORES["minor_issue"])
            
            # Calculate score based on flags
            critical_flags = ["INVALID_PAN_FORMAT", "INVALID_AADHAAR_FORMAT"]
            minor_flags = ["INCONSISTENT_DATE_FORMATS", "MINIMAL_TEXT_CONTENT"]
            
            for flag in flags:
                if any(cf in flag for cf in critical_flags):
                    score = min(score, DEFAULT_SCORES["moderate_issue"])
                elif any(mf in flag for mf in minor_flags):
                    score = min(score, DEFAULT_SCORES["minor_issue"])
            
        except Exception as e:
            logger.warning(f"Text analysis failed: {e}")
            return LayerResult(
                name="text",
                score=DEFAULT_SCORES["minor_issue"],
                flags=["ANALYSIS_ERROR"],
                details={"error": str(e)},
            )
        
        return LayerResult(
            name="text",
            score=score,
            flags=flags,
            details=details,
        )
    
    def _check_pan_format(self, text: str) -> Tuple[List[str], int]:
        """
        Check PAN format (not existence).
        
        Valid PAN: 5 letters + 4 digits + 1 letter
        4th char must be valid entity type.
        """
        flags = []
        valid_count = 0
        
        # Find all PAN-like patterns
        pan_pattern = r'[A-Z]{5}[0-9]{4}[A-Z]'
        pans = re.findall(pan_pattern, text.upper())
        
        for pan in pans:
            # Check 4th character (entity type)
            if pan[3] in VALID_PAN_ENTITY_TYPES:
                valid_count += 1
            else:
                flags.append(f"INVALID_PAN_FORMAT: {pan[:4]}****")
        
        return flags, valid_count
    
    def _check_aadhaar_format(self, text: str) -> Tuple[List[str], int]:
        """
        Check Aadhaar format (not existence).
        
        Valid: 12 digits, no leading 0 or 1.
        """
        flags = []
        valid_count = 0
        
        # Find 12-digit sequences
        aadhaar_like = re.findall(r'\b\d{12}\b', text)
        
        for num in aadhaar_like:
            if re.match(AADHAAR_PATTERN, num):
                valid_count += 1
            elif num[0] in '01':
                flags.append("INVALID_AADHAAR_FORMAT: starts with 0/1")
        
        return flags, valid_count
    
    def _check_date_consistency(self, text: str) -> List[str]:
        """
        Check date format consistency.
        
        Flags if document uses both DD/MM/YYYY and YYYY-MM-DD.
        """
        flags = []
        
        dates_slash = re.findall(r'\d{1,2}/\d{1,2}/\d{2,4}', text)
        dates_dash = re.findall(r'\d{1,2}-\d{1,2}-\d{2,4}', text)
        
        # Both formats used = potential splicing
        if dates_slash and dates_dash:
            if len(dates_slash) > 0 and len(dates_dash) > 0:
                flags.append("INCONSISTENT_DATE_FORMATS")
        
        return flags
