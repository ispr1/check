"""
VerificationStep model - represents individual verification steps within a session.

Each step tracks: type, mandatory/optional, status, input data, and completion.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Enum,
    Index,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..database import Base


class StepType(str, enum.Enum):
    """Types of verification steps."""
    PERSONAL_INFO = "PERSONAL_INFO"
    FACE_LIVENESS = "FACE_LIVENESS"
    AADHAAR = "AADHAAR"
    PAN = "PAN"
    UAN = "UAN"
    EDUCATION = "EDUCATION"
    EXPERIENCE = "EXPERIENCE"


class StepStatus(str, enum.Enum):
    """Status of a verification step."""
    PENDING = "PENDING"       # Not yet completed
    COMPLETED = "COMPLETED"   # Successfully completed
    FAILED = "FAILED"         # Failed verification (e.g., mismatch)
    SKIPPED = "SKIPPED"       # Skipped (optional step not applicable)


# Mandatory steps that every verification must have
MANDATORY_STEPS = [
    StepType.PERSONAL_INFO,
    StepType.FACE_LIVENESS,
    StepType.AADHAAR,
    StepType.PAN,
]

# Conditional steps (created based on candidate profile)
CONDITIONAL_STEPS = [
    StepType.UAN,
    StepType.EDUCATION,
    StepType.EXPERIENCE,
]


class VerificationStep(Base):
    """
    Individual verification step within a verification session.
    
    Stores candidate input data and (later) vendor responses.
    Score contribution is calculated in Phase 4.
    
    Phase 2.5 additions:
    - flags: Separate flags storage (overlaps, mismatches)
    - source: Who verified (surepass, manual)
    - verified_at: When truth was fetched
    - review_assets: HR-viewable files (not encrypted)
    - hr_notes: HR can document decisions
    - audit_trail: Action history per step
    """
    __tablename__ = "verification_steps"

    id = Column(Integer, primary_key=True, index=True)
    
    verification_id = Column(
        Integer,
        ForeignKey("verifications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Step type from enum
    step_type = Column(
        Enum(StepType),
        nullable=False,
    )
    
    # Whether this step is mandatory for submission
    is_mandatory = Column(Boolean, nullable=False, default=True)
    
    # Current status
    status = Column(
        Enum(StepStatus),
        nullable=False,
        default=StepStatus.PENDING,
    )
    
    # Candidate-submitted data (encrypted at rest via app-level encryption)
    input_data = Column(JSONB, nullable=True)
    
    # Vendor API response (ENCRYPTED - Phase 2.5)
    # Contains government identity data - never exposed to HR
    raw_response = Column(JSONB, nullable=True)
    
    # Score contribution (Phase 4, calculated after submission)
    score_contribution = Column(Integer, nullable=True)
    
    # ============ Phase 2.5 Hardening Columns ============
    
    # Flags for HR review (NOT encrypted - visible to HR)
    # Example: ["OVERLAPPING_EMPLOYMENT", "EXPERIENCE_MISMATCH"]
    flags = Column(JSONB, nullable=True, default=list)
    
    # Source of verification truth
    # Example: "surepass", "manual", "document"
    source = Column(String(50), nullable=True)
    
    # When truth was fetched from external source
    verified_at = Column(DateTime, nullable=True)
    
    # HR-viewable assets (NOT encrypted)
    # Example: {"face_images": ["s3://..."], "payslips": ["s3://..."]}
    review_assets = Column(JSONB, nullable=True)
    
    # HR notes for manual review decisions
    hr_notes = Column(String(2000), nullable=True)
    
    # Audit trail for compliance (NOT encrypted)
    # Example: [{"timestamp": "...", "action": "VERIFIED", "actor": "SYSTEM"}]
    audit_trail = Column(JSONB, nullable=True, default=list)
    
    # ============ Timestamps ============
    
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    verification = relationship("Verification", back_populates="steps")

    # Indexes
    __table_args__ = (
        Index("ix_verification_steps_verification_type", "verification_id", "step_type"),
    )

    def mark_completed(self, input_data: dict = None):
        """Mark step as completed with optional input data."""
        self.status = StepStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        if input_data:
            self.input_data = input_data

    def mark_failed(self, input_data: dict = None):
        """Mark step as failed."""
        self.status = StepStatus.FAILED
        self.completed_at = datetime.utcnow()
        if input_data:
            self.input_data = input_data

    def mark_skipped(self):
        """Mark step as skipped (for optional steps)."""
        if not self.is_mandatory:
            self.status = StepStatus.SKIPPED
            self.completed_at = datetime.utcnow()
