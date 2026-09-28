from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Jane Recruiter")
    email: EmailStr = Field(..., example="jane.recruiter@company.com")
    role: UserRole = Field(default=UserRole.CANDIDATE, example=UserRole.RECRUITER)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128, example="SecurePassword123!")


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="jane.recruiter@company.com")
    password: str = Field(..., example="SecurePassword123!")


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[str] = None
