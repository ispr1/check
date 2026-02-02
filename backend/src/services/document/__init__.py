"""
Document Analysis Service Package.

Phase 4: Open-source document forensics for legitimacy scoring.
"""

from .service import DocumentAnalysisService, get_document_service
from .contracts import (
    DocumentAnalysisResult,
    DocumentStatus,
    DocumentType,
    LayerResult,
)

__all__ = [
    "DocumentAnalysisService",
    "get_document_service",
    "DocumentAnalysisResult",
    "DocumentStatus",
    "DocumentType",
    "LayerResult",
]
