from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class OAuthLoginRequest(BaseModel):
    """OAuth login request (Google/Apple)"""
    provider: str = Field(..., description="google yoki apple")
    id_token: str = Field(..., description="OAuth provider dan olingan ID token")
    access_token: Optional[str] = Field(None, description="Access token (Google uchun)")

class OAuthUserInfo(BaseModel):
    """OAuth provider dan olingan user ma'lumotlari"""
    provider_user_id: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    picture: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None

class TokenResponse(BaseModel):
    """Login response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    email: Optional[str] = None
    role: str