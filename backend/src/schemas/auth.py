from pydantic import BaseModel, EmailStr
from datetime import datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str
    full_name: str
    role: str
    company_id: int


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    company_id: int

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    user_id: int
    email: str
    company_id: int
    role: str
