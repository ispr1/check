"""
FaceComparison model.

Stores face comparison results for audit and HR review.
Raw Rekognition response is encrypted and never exposed to HR.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    LargeBinary,
    Index,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base


class FaceComparison(Base):
    """
    Face comparison result record.
    
    Stores:
    - Decision (MATCH, LOW_CONFIDENCE, MISMATCH, etc.)
    - Confidence score
    - S3 keys for images
    - Encrypted raw API response
    - Audit trail
    
    HR can view:
    - Decision
    - Confidence score
    - Presigned URLs to images
    
    HR cannot view:
    - Raw vendor response
    """
    __tablename__ = "face_comparisons"

    id = Column(Integer, primary_key=True, index=True)
    
    # Link to verification
    verification_id = Column(
        Integer,
        ForeignKey("verifications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Link to verification step (FACE_LIVENESS)
    step_id = Column(
        Integer,
        ForeignKey("verification_steps.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    
    # Link to candidate
    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # ============ Evidence (Images) ============
    
    # S3 keys for images
    selfie_s3_key = Column(String(500), nullable=False)
    reference_s3_key = Column(String(500), nullable=True)
    
    # Source of reference image
    reference_source = Column(String(50), nullable=True)  # hr_upload, aadhaar, id_card
    
    # ============ Truth (Scores) ============
    
    # Confidence from vendor (0-100)
    confidence_score = Column(Float, nullable=False, default=0.0)
    
    # Decision based on thresholds
    # MATCH, LOW_CONFIDENCE, MISMATCH, PENDING_REFERENCE, NOT_AVAILABLE, ERROR
    decision = Column(String(50), nullable=False)
    
    # Flags for HR review
    flags = Column(JSONB, nullable=True, default=list)
    
    # ============ Encrypted Data (Never Exposed) ============
    
    # Raw vendor response - ENCRYPTED
    # Store as bytes, encrypted at application level
    raw_response_encrypted = Column(LargeBinary, nullable=True)
    
    # ============ Audit ============
    
    # Who triggered comparison
    triggered_by = Column(String(100), nullable=True)  # "candidate", "hr_upload", "system"
    
    # Audit trail
    audit_trail = Column(JSONB, nullable=True, default=list)
    
    # ============ Timestamps ============
    
    compared_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Indexes
    __table_args__ = (
        Index("ix_face_comparisons_verification_candidate", "verification_id", "candidate_id"),
    )

    def to_hr_view(self) -> dict:
        """Return HR-safe view (no raw response)."""
        return {
            "id": self.id,
            "candidate_id": self.candidate_id,
            "decision": self.decision,
            "confidence_score": round(self.confidence_score, 1),
            "reference_source": self.reference_source,
            "flags": self.flags or [],
            "compared_at": self.compared_at.isoformat() if self.compared_at else None,
        }
    
    def add_audit_entry(self, action: str, actor: str, details: dict = None):
        """Add audit trail entry."""
        if self.audit_trail is None:
            self.audit_trail = []
        
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "actor": actor,
        }
        if details:
            entry["details"] = details
        
        self.audit_trail.append(entry)
