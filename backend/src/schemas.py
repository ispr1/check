from pydantic import BaseModel, EmailStr
from datetime import datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    role: str


class UserResponse(BaseModel):
    """Public user profile response"""

    id: int
    email: EmailStr
    role: str
    company_id: int
    created_at: datetime

    class Config:
        from_attributes = True
