"""
Document Analysis Service.

Orchestrates multi-layer document forensics.
"""

import logging
from datetime import datetime
from typing import Optional

from .contracts import (
    DocumentAnalysisResult,
    DocumentStatus,
    DocumentType,
    LayerResult,
)
from .rules import WEIGHTS, THRESHOLDS, DEFAULT_SCORES
from .analyzers import (
    MetadataAnalyzer,
    FontAnalyzer,
    TextAnalyzer,
    ForensicsAnalyzer,
)

logger = logging.getLogger(__name__)


class DocumentAnalysisService:
    """
    Multi-layer document forensics service.
    
    Combines metadata, font, text, and forensics analysis
    to calculate legitimacy score.
    """
    
    def __init__(self):
        self.metadata_analyzer = MetadataAnalyzer()
        self.font_analyzer = FontAnalyzer()
        self.text_analyzer = TextAnalyzer()
        self.forensics_analyzer = ForensicsAnalyzer()
        
        logger.info("DocumentAnalysisService initialized")
    
    def analyze(
        self,
        file_bytes: bytes,
        doc_type: str = "other",
    ) -> DocumentAnalysisResult:
        """
        Perform complete document analysis.
        
        Args:
            file_bytes: PDF file as bytes
            doc_type: Type of document (education, experience, id_card, other)
            
        Returns:
            DocumentAnalysisResult with legitimacy score and breakdown
        """
        layer_results = []
        all_flags = []
        breakdown = {}
        
        # Layer 1: Metadata analysis
        metadata_result = self.metadata_analyzer.analyze(file_bytes)
        layer_results.append(metadata_result)
        all_flags.extend(metadata_result.flags)
        breakdown["metadata"] = metadata_result.score
        
        # Layer 2: Font analysis
        font_result = self.font_analyzer.analyze(file_bytes)
        layer_results.append(font_result)
        all_flags.extend(font_result.flags)
        breakdown["fonts"] = font_result.score
        
        # Layer 3: Text analysis
        text_result = self.text_analyzer.analyze(file_bytes, doc_type)
        layer_results.append(text_result)
        all_flags.extend(text_result.flags)
        breakdown["text"] = text_result.score
        
        # Layer 4: Forensics analysis
        forensics_result = self.forensics_analyzer.analyze(file_bytes)
        layer_results.append(forensics_result)
        all_flags.extend(forensics_result.flags)
        breakdown["forensics"] = forensics_result.score
        
        # Calculate weighted score
        legitimacy_score = self._calculate_weighted_score(breakdown)
        
        # Determine status
        status = self._get_status(legitimacy_score)
        
        # Get page count from text result
        page_count = text_result.details.get("page_count", 0)
        
        return DocumentAnalysisResult(
            legitimacy_score=legitimacy_score,
            status=status,
            flags=list(set(all_flags)),  # Dedupe
            breakdown=breakdown,
            layer_results=layer_results,
            analyzed_at=datetime.utcnow(),
            document_type=DocumentType(doc_type) if doc_type in [e.value for e in DocumentType] else DocumentType.OTHER,
            page_count=page_count,
        )
    
    def _calculate_weighted_score(self, breakdown: dict) -> float:
        """
        Calculate weighted legitimacy score.
        
        Uses centralized weights from rules.py.
        """
        total = 0.0
        
        for layer, weight in WEIGHTS.items():
            score = breakdown.get(layer, DEFAULT_SCORES["clean"])
            total += score * weight
        
        return round(total, 2)
    
    def _get_status(self, score: float) -> DocumentStatus:
        """
        Determine status based on score thresholds.
        """
        if score >= THRESHOLDS["legitimate"]:
            return DocumentStatus.LEGITIMATE
        elif score >= THRESHOLDS["review_required"]:
            return DocumentStatus.REVIEW_REQUIRED
        else:
            return DocumentStatus.SUSPICIOUS


# Singleton instance
_service_instance: Optional[DocumentAnalysisService] = None


def get_document_service() -> DocumentAnalysisService:
    """Get or create singleton DocumentAnalysisService."""
    global _service_instance
    if _service_instance is None:
        _service_instance = DocumentAnalysisService()
    return _service_instance
