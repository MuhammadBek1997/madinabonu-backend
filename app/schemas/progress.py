from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VideoProgressCreate(BaseModel):
    """Video progress yaratish/yangilash"""
    video_id: int
    progress_seconds: int
    completed: bool = False
    completion_percentage: float = 0.0

class VideoProgressResponse(BaseModel):
    """Video progress response"""
    id: int
    user_id: int
    video_id: int
    progress_seconds: int
    completed: bool
    completion_percentage: float
    last_watched: datetime
    created_at: datetime

    class Config:
        from_attributes = True
