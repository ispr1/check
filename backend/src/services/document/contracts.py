"""
Document analysis contracts and types.

Result types for document analysis.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime


class DocumentStatus(str, Enum):
    """Document analysis status."""
    LEGITIMATE = "LEGITIMATE"           # Score >= 85
    REVIEW_REQUIRED = "REVIEW_REQUIRED"  # Score 60-84
    SUSPICIOUS = "SUSPICIOUS"            # Score < 60
    ERROR = "ERROR"                      # Analysis failed
    PENDING = "PENDING"                  # Not yet analyzed


class DocumentType(str, Enum):
    """Supported document types."""
    EDUCATION = "education"
    EXPERIENCE = "experience"
    ID_CARD = "id_card"
    OTHER = "other"


@dataclass
class LayerResult:
    """Result from a single analysis layer."""
    name: str
    score: float  # 0-100
    flags: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "score": round(self.score, 1),
            "flags": self.flags,
        }


@dataclass
class DocumentAnalysisResult:
    """Complete document analysis result."""
    legitimacy_score: float
    status: DocumentStatus
    flags: List[str] = field(default_factory=list)
    breakdown: Dict[str, float] = field(default_factory=dict)
    layer_results: List[LayerResult] = field(default_factory=list)
    analyzed_at: Optional[datetime] = None
    document_type: Optional[DocumentType] = None
    page_count: int = 0
    
    def to_hr_view(self) -> Dict[str, Any]:
        """Return HR-safe summary (no raw forensic data)."""
        return {
            "legitimacy_score": round(self.legitimacy_score, 1),
            "status": self.status.value,
            "flags": self.flags,
            "breakdown": {k: round(v, 1) for k, v in self.breakdown.items()},
            "analyzed_at": self.analyzed_at.isoformat() if self.analyzed_at else None,
        }
    
    def to_audit(self) -> Dict[str, Any]:
        """Full audit record."""
        return {
            "legitimacy_score": self.legitimacy_score,
            "status": self.status.value,
            "flags": self.flags,
            "breakdown": self.breakdown,
            "layers": [lr.to_dict() for lr in self.layer_results],
            "document_type": self.document_type.value if self.document_type else None,
            "page_count": self.page_count,
            "analyzed_at": self.analyzed_at.isoformat() if self.analyzed_at else None,
        }
