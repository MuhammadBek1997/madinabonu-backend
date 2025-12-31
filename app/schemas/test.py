from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class TestQuestionCreate(BaseModel):
    """Test savol yaratish"""
    question_text: str
    options: List[str]
    correct_answer: int
    image_url: Optional[str] = None
    explanation: Optional[str] = None
    order: int = 0

class TestQuestionResponse(BaseModel):
    """Test savol response"""
    id: int
    question_text: str
    options: List[str]
    correct_answer: int
    image_url: Optional[str] = None
    explanation: Optional[str] = None
    order: int

    class Config:
        from_attributes = True

class TestCreate(BaseModel):
    """Test yaratish"""
    title: str
    description: Optional[str] = None
    video_id: Optional[int] = None
    category: Optional[str] = None
    subject: Optional[str] = None
    time_limit: int = 600
    passing_score: int = 70
    is_published: bool = True
    questions: List[TestQuestionCreate] = []

class TestResponse(BaseModel):
    """Test response"""
    id: int
    title: str
    description: Optional[str] = None
    video_id: Optional[int] = None
    category: Optional[str] = None
    subject: Optional[str] = None
    time_limit: int
    passing_score: int
    is_published: bool
    created_at: datetime
    questions: List[TestQuestionResponse] = []

    class Config:
        from_attributes = True

class TestResultCreate(BaseModel):
    """Test natija yuborish"""
    test_id: int
    answers: List[int]  # foydalanuvchi javoblari [0, 2, 1, 3, ...]
    time_spent: Optional[int] = None

class TestResultResponse(BaseModel):
    """Test natija response"""
    id: int
    user_id: int
    test_id: int
    score: int
    total_questions: int
    percentage: int
    passed: bool
    time_spent: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
