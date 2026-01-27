from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    users = relationship("User", back_populates="company", cascade="all, delete-orphan")
    candidates = relationship(
        "Candidate", back_populates="company", cascade="all, delete-orphan"
    )
    verification_requests = relationship(
        "VerificationRequest", back_populates="company", cascade="all, delete-orphan"
    )
    verifications = relationship(
        "Verification", back_populates="company", cascade="all, delete-orphan"
    )

