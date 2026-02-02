"""
DocumentVerification model.

Stores document analysis results for audit and HR review.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

from ..database import Base


class DocumentVerification(Base):
    """
    Document analysis result record.
    
    Stores:
    - Legitimacy score (0-100)
    - Status (LEGITIMATE, REVIEW_REQUIRED, SUSPICIOUS)
    - Layer breakdown
    - Flags
    """
    __tablename__ = "document_verifications"

    id = Column(Integer, primary_key=True, index=True)
    
    # Link to verification
    verification_id = Column(
        Integer,
        ForeignKey("verifications.id", ondelete="CASCADE"),
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
    
    # Document info
    document_type = Column(String(50), nullable=False)  # education, experience, id_card
    s3_key = Column(String(500), nullable=False)
    original_filename = Column(String(255), nullable=True)
    
    # Analysis results
    legitimacy_score = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=False)  # LEGITIMATE, REVIEW_REQUIRED, SUSPICIOUS
    
    # Breakdown by layer
    breakdown = Column(JSONB, nullable=True, default=dict)
    
    # Flags for HR review
    flags = Column(JSONB, nullable=True, default=list)
    
    # Audit
    analyzed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Indexes
    __table_args__ = (
        Index("ix_doc_verifications_candidate_type", "candidate_id", "document_type"),
    )

    def to_hr_view(self) -> dict:
        """Return HR-safe view."""
        return {
            "id": self.id,
            "document_type": self.document_type,
            "legitimacy_score": round(self.legitimacy_score, 1),
            "status": self.status,
            "flags": self.flags or [],
            "breakdown": {k: round(v, 1) for k, v in (self.breakdown or {}).items()},
            "analyzed_at": self.analyzed_at.isoformat() if self.analyzed_at else None,
        }
