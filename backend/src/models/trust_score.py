"""
TrustScore models.

Stores calculated scores and HR overrides.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    Index,
)
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from datetime import datetime

from ..database import Base


class TrustScore(Base):
    """
    Trust score record for a verification.
    
    Stores:
    - Calculated score (0-100)
    - Status (VERIFIED, REVIEW_REQUIRED, HIGH_RISK, FLAGGED)
    - Component breakdown
    - Flags and recommendations
    """
    __tablename__ = "trust_scores"

    id = Column(Integer, primary_key=True, index=True)
    
    # Link to verification
    verification_id = Column(
        Integer,
        ForeignKey("verifications.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    
    # Link to candidate
    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Score and status
    score = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=False)  # VERIFIED, REVIEW_REQUIRED, etc.
    
    # Completion
    completion_rate = Column(Float, nullable=False, default=0.0)
    
    # Component breakdown
    breakdown = Column(JSONB, nullable=True, default=dict)
    
    # Flags
    flags = Column(JSONB, nullable=True, default=list)
    
    # Recommendations for HR
    recommendations = Column(JSONB, nullable=True, default=list)
    
    # Override tracking
    is_overridden = Column(Boolean, default=False)
    override_id = Column(Integer, ForeignKey("trust_score_overrides.id"), nullable=True)
    
    # Timestamps
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Indexes
    __table_args__ = (
        Index("ix_trust_scores_candidate_status", "candidate_id", "status"),
    )

    def to_hr_view(self) -> dict:
        """Return HR-safe view."""
        return {
            "id": self.id,
            "verification_id": self.verification_id,
            "score": round(self.score, 1),
            "status": self.status,
            "completion_rate": round(self.completion_rate * 100, 1),
            "breakdown": {k: round(v, 1) for k, v in (self.breakdown or {}).items()},
            "flags": self.flags or [],
            "recommendations": self.recommendations or [],
            "is_overridden": self.is_overridden,
            "calculated_at": self.calculated_at.isoformat() if self.calculated_at else None,
        }


class TrustScoreOverride(Base):
    """
    Trust score override audit record.
    
    Logs when HR overrides a score decision.
    """
    __tablename__ = "trust_score_overrides"

    id = Column(Integer, primary_key=True, index=True)
    
    # Link to trust score
    trust_score_id = Column(
        Integer,
        ForeignKey("trust_scores.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Before override
    original_score = Column(Float, nullable=False)
    original_status = Column(String(50), nullable=False)
    original_flags = Column(JSONB, nullable=True)
    
    # Override decision
    overridden_status = Column(String(50), nullable=False)  # APPROVED, REJECTED
    
    # Audit info
    overridden_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    override_reason = Column(Text, nullable=False)
    override_category = Column(String(50), nullable=False)  # FALSE_POSITIVE, EXPLAINABLE, etc.
    
    # Supporting evidence
    supporting_documents = Column(JSONB, nullable=True)  # S3 keys of additional docs
    notes = Column(Text, nullable=True)
    
    # Approval chain (for scores < 50)
    requires_senior_approval = Column(Boolean, default=False)
    senior_approved_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    senior_approved_at = Column(DateTime, nullable=True)
    senior_notes = Column(Text, nullable=True)
    
    # Timestamps
    overridden_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Indexes
    __table_args__ = (
        Index("ix_trust_overrides_by_user", "overridden_by"),
    )

    def to_audit(self) -> dict:
        """Return audit record."""
        return {
            "id": self.id,
            "trust_score_id": self.trust_score_id,
            "original_score": self.original_score,
            "original_status": self.original_status,
            "overridden_status": self.overridden_status,
            "override_reason": self.override_reason,
            "override_category": self.override_category,
            "overridden_by": self.overridden_by,
            "overridden_at": self.overridden_at.isoformat() if self.overridden_at else None,
            "requires_senior_approval": self.requires_senior_approval,
            "senior_approved_by": self.senior_approved_by,
            "senior_approved_at": self.senior_approved_at.isoformat() if self.senior_approved_at else None,
        }
