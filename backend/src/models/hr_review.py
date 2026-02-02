"""
HR Review Models.

Phase 6: HR document uploads and hiring decisions.
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
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from datetime import datetime
from enum import Enum

from ..database import Base


class HRDecisionStatus(str, Enum):
    """HR decision status."""
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    NEED_MORE_INFO = "NEED_MORE_INFO"
    PENDING = "PENDING"


class HRDocument(Base):
    """
    HR-uploaded document record.
    
    For documents uploaded by HR after candidate submission:
    - Missing certificates
    - Clarification documents
    - Experience proofs
    - Bonafide letters
    """
    __tablename__ = "hr_documents"

    id = Column(Integer, primary_key=True, index=True)
    
    # Links
    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    verification_id = Column(
        Integer,
        ForeignKey("verifications.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    
    # Document info
    document_type = Column(String(50), nullable=False)  # education, experience, clarification
    s3_key = Column(String(500), nullable=False)
    original_filename = Column(String(255), nullable=True)
    
    # Source tracking
    source = Column(String(50), default="hr_upload")  # Always hr_upload for this table
    uploaded_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # HR notes
    notes = Column(Text, nullable=True)
    
    # Analysis results (linked to document_verifications)
    document_verification_id = Column(
        Integer,
        ForeignKey("document_verifications.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Status
    is_analyzed = Column(Boolean, default=False)
    analysis_status = Column(String(50), nullable=True)  # LEGITIMATE, REVIEW_REQUIRED, SUSPICIOUS
    legitimacy_score = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Indexes
    __table_args__ = (
        Index("ix_hr_documents_candidate_type", "candidate_id", "document_type"),
    )

    def to_hr_view(self) -> dict:
        """Return HR-safe view."""
        return {
            "id": self.id,
            "document_type": self.document_type,
            "original_filename": self.original_filename,
            "source": self.source,
            "notes": self.notes,
            "is_analyzed": self.is_analyzed,
            "analysis_status": self.analysis_status,
            "legitimacy_score": round(self.legitimacy_score, 1) if self.legitimacy_score else None,
            "uploaded_at": self.created_at.isoformat() if self.created_at else None,
        }


class HRDecision(Base):
    """
    HR hiring decision record.
    
    Immutable audit trail of HR decisions.
    """
    __tablename__ = "hr_decisions"

    id = Column(Integer, primary_key=True, index=True)
    
    # Links
    verification_id = Column(
        Integer,
        ForeignKey("verifications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Decision
    decision = Column(String(50), nullable=False)  # APPROVED, REJECTED, NEED_MORE_INFO
    
    # Decision maker
    decided_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    decided_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Reasoning
    reason_codes = Column(JSONB, default=list)  # ["DOCUMENT_ISSUES", "FACE_MISMATCH"]
    comments = Column(Text, nullable=True)
    
    # Override tracking
    override_requested = Column(Boolean, default=False)
    override_approved_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    override_approved_at = Column(DateTime, nullable=True)
    override_comments = Column(Text, nullable=True)
    
    # Trust score snapshot (immutable record)
    trust_score_at_decision = Column(Float, nullable=True)
    trust_status_at_decision = Column(String(50), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Indexes
    __table_args__ = (
        Index("ix_hr_decisions_verification", "verification_id"),
        Index("ix_hr_decisions_candidate", "candidate_id"),
    )

    def to_audit(self) -> dict:
        """Return full audit record."""
        return {
            "id": self.id,
            "verification_id": self.verification_id,
            "candidate_id": self.candidate_id,
            "decision": self.decision,
            "decided_by": self.decided_by,
            "decided_at": self.decided_at.isoformat() if self.decided_at else None,
            "reason_codes": self.reason_codes or [],
            "comments": self.comments,
            "override_requested": self.override_requested,
            "override_approved_by": self.override_approved_by,
            "trust_score_at_decision": self.trust_score_at_decision,
            "trust_status_at_decision": self.trust_status_at_decision,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
