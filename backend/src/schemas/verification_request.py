from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class VerificationRequestCreate(BaseModel):
    candidate_id: int = Field(..., gt=0, description="ID of the candidate to verify")


class VerificationRequestResponse(BaseModel):
    id: int
    candidate_id: int
    company_id: int
    status: str
    created_at: datetime

    # Nested candidate info
    candidate_name: Optional[str] = None

    class Config:
        from_attributes = True


class VerificationRequestListItem(BaseModel):
    id: int
    candidate_id: int
    candidate_name: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
