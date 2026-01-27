"""
Verification model - represents a verification session for a candidate.

Status flow: CREATED → LINK_SENT → IN_PROGRESS → SUBMITTED → SCORED
Token expires after 7 days. Session is resumable until expiry or submission.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Index,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import enum
import secrets

from ..database import Base


class VerificationStatus(str, enum.Enum):
    """Status of a verification session."""
    CREATED = "CREATED"           # Initial state after HR creates
    LINK_SENT = "LINK_SENT"       # Link generated and sent to candidate
    IN_PROGRESS = "IN_PROGRESS"   # Candidate has accessed and started
    SUBMITTED = "SUBMITTED"       # Candidate completed all steps and submitted
    SCORED = "SCORED"             # Trust score calculated (Phase 4)


def generate_verification_token() -> str:
    """Generate a secure 64-character random token."""
    return secrets.token_urlsafe(48)  # 48 bytes = 64 chars base64


def get_token_expiry() -> datetime:
    """Get expiry datetime 7 days from now."""
    return datetime.utcnow() + timedelta(days=7)


class Verification(Base):
    """
    Verification session for a candidate.
    
    One candidate can have only one active verification at a time.
    Token is single-use after submission.
    """
    __tablename__ = "verifications"

    id = Column(Integer, primary_key=True, index=True)
    
    # One-to-one with candidate (unique constraint)
    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # One verification per candidate
        index=True,
    )
    
    # Company for easy querying (denormalized from candidate)
    company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Secure token for candidate access
    token = Column(
        String(100),
        unique=True,
        nullable=False,
        default=generate_verification_token,
        index=True,
    )
    
    # Token expires after 7 days
    token_expires_at = Column(
        DateTime,
        nullable=False,
        default=get_token_expiry,
    )
    
    # Status tracking
    status = Column(
        Enum(VerificationStatus),
        nullable=False,
        default=VerificationStatus.CREATED,
        index=True,
    )
    
    # Trust score - NULL until SUBMITTED, calculated in Phase 4
    trust_score = Column(Integer, nullable=True)
    trust_score_details = Column(JSONB, nullable=True)
    
    # Timestamps
    submitted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    candidate = relationship("Candidate", back_populates="verification")
    company = relationship("Company", back_populates="verifications")
    steps = relationship(
        "VerificationStep",
        back_populates="verification",
        cascade="all, delete-orphan",
        order_by="VerificationStep.id",
    )

    # Composite indexes for common queries
    __table_args__ = (
        Index("ix_verifications_company_status", "company_id", "status"),
    )

    def is_expired(self) -> bool:
        """Check if the verification token has expired."""
        return datetime.utcnow() > self.token_expires_at

    def can_be_modified(self) -> bool:
        """Check if verification can still accept step updates."""
        return (
            not self.is_expired()
            and self.status not in [VerificationStatus.SUBMITTED, VerificationStatus.SCORED]
        )
