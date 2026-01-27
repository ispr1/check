from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base  # Fixed: changed from .database to ..database


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    full_name = Column(String(255), nullable=False)
    dob = Column(Date, nullable=False)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    company = relationship("Company", back_populates="candidates")
    verification_requests = relationship(
        "VerificationRequest", back_populates="candidate", cascade="all, delete-orphan"
    )
    # One-to-one relationship with Verification
    verification = relationship(
        "Verification", back_populates="candidate", uselist=False, cascade="all, delete-orphan"
    )

    # Unique constraint: email + company_id
    __table_args__ = (
        UniqueConstraint("email", "company_id", name="uq_candidate_email_company"),
    )
