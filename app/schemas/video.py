from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VideoCategoryCreate(BaseModel):
    """Video kategoriya yaratish"""
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    order: int = 0

class VideoCategoryResponse(BaseModel):
    """Video kategoriya response"""
    id: int
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    order: int
    created_at: datetime

    class Config:
        from_attributes = True

class VideoCreate(BaseModel):
    """Video yaratish"""
    title: str
    description: Optional[str] = None
    video_url: str
    thumbnail_url: Optional[str] = None
    duration: Optional[int] = None
    category_id: Optional[int] = None
    subject: Optional[str] = None
    is_published: bool = True
    order: int = 0

class VideoResponse(BaseModel):
    """Video response"""
    id: int
    title: str
    description: Optional[str] = None
    video_url: str
    thumbnail_url: Optional[str] = None
    duration: Optional[int] = None
    category_id: Optional[int] = None
    subject: Optional[str] = None
    is_published: bool
    order: int
    views_count: int
    created_at: datetime
    category: Optional[VideoCategoryResponse] = None

    class Config:
        from_attributes = True
