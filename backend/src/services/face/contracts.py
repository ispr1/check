"""
Face verification contracts and types.

Defines result types, decisions, and reference sources.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime


class FaceDecision(str, Enum):
    """Face comparison decision based on confidence thresholds."""
    MATCH = "MATCH"              # ≥90% confidence
    LOW_CONFIDENCE = "LOW_CONFIDENCE"  # 70-89% confidence
    MISMATCH = "MISMATCH"        # <70% confidence
    PENDING_REFERENCE = "PENDING_REFERENCE"  # No reference image yet
    NOT_AVAILABLE = "NOT_AVAILABLE"  # Provider unavailable
    ERROR = "ERROR"              # Processing error


class ReferenceSource(str, Enum):
    """Source of face reference image."""
    HR_UPLOAD = "hr_upload"      # HR uploaded reference
    AADHAAR = "aadhaar"          # From Aadhaar (via Surepass/DigiLocker)
    ID_CARD = "id_card"          # Company ID card
    INTERVIEW = "interview"      # Interview system (future)
    OTHER = "other"


# Confidence thresholds
CONFIDENCE_MATCH_THRESHOLD = 90.0
CONFIDENCE_LOW_THRESHOLD = 70.0


def get_decision_from_confidence(confidence: float) -> FaceDecision:
    """
    Map confidence score to decision.
    
    ≥90% → MATCH
    70-89% → LOW_CONFIDENCE
    <70% → MISMATCH
    """
    if confidence >= CONFIDENCE_MATCH_THRESHOLD:
        return FaceDecision.MATCH
    elif confidence >= CONFIDENCE_LOW_THRESHOLD:
        return FaceDecision.LOW_CONFIDENCE
    else:
        return FaceDecision.MISMATCH


@dataclass
class FaceCompareResult:
    """Result of a face comparison operation."""
    decision: FaceDecision
    confidence_score: float
    reference_source: ReferenceSource
    selfie_s3_key: str
    reference_s3_key: Optional[str]
    flags: List[str] = field(default_factory=list)
    compared_at: Optional[datetime] = None
    
    # URLs for HR view (presigned, expires)
    selfie_url: Optional[str] = None
    reference_url: Optional[str] = None
    
    # Never expose to HR
    raw_response_encrypted: Optional[bytes] = None
    
    def to_hr_view(self) -> Dict[str, Any]:
        """Return HR-safe view (no raw response)."""
        return {
            "decision": self.decision.value,
            "confidence_score": round(self.confidence_score, 1),
            "reference_source": self.reference_source.value,
            "selfie_url": self.selfie_url,
            "reference_url": self.reference_url,
            "flags": self.flags,
            "compared_at": self.compared_at.isoformat() if self.compared_at else None,
        }
    
    def to_audit(self) -> Dict[str, Any]:
        """Return full audit record (raw response excluded from dict, stored separately)."""
        return {
            "decision": self.decision.value,
            "confidence_score": self.confidence_score,
            "reference_source": self.reference_source.value,
            "selfie_s3_key": self.selfie_s3_key,
            "reference_s3_key": self.reference_s3_key,
            "flags": self.flags,
            "compared_at": self.compared_at.isoformat() if self.compared_at else None,
        }


@dataclass
class FaceNotAvailableResult:
    """Result when face verification is not available."""
    decision: FaceDecision = FaceDecision.NOT_AVAILABLE
    confidence_score: float = 0.0
    message: str = "Face verification service unavailable"
    
    def to_hr_view(self) -> Dict[str, Any]:
        return {
            "decision": self.decision.value,
            "confidence_score": 0.0,
            "message": self.message,
        }
