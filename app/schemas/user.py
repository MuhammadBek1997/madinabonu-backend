from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.enums import UserRole

class UserCreate(BaseModel):
    """User yaratish uchun schema"""
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: str
    role: UserRole = UserRole.CLIENT  # Default: oddiy foydalanuvchi

class UserLogin(BaseModel):
    """Login schema"""
    username: str
    password: str

class UserResponse(BaseModel):
    """User response schema"""
    id: int
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    """JWT Token response"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Token ichidagi ma'lumot"""
    username: Optional[str] = None
    user_id: Optional[int] = None
