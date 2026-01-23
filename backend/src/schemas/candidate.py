from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional


class CandidateCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    dob: date
    email: Optional[EmailStr] = None


class CandidateResponse(BaseModel):
    id: int
    full_name: str
    dob: date
    email: Optional[str]
    company_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CandidateListItem(BaseModel):
    id: int
    full_name: str
    created_at: datetime
    trust_score: Optional[float] = None

    class Config:
        from_attributes = True
