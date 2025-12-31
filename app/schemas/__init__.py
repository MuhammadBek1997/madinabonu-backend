from app.schemas.user import UserCreate, UserLogin, UserResponse, Token, TokenData
from app.schemas.video import VideoCreate, VideoResponse, VideoCategoryCreate, VideoCategoryResponse
from app.schemas.test import TestCreate, TestResponse, TestQuestionCreate, TestQuestionResponse, TestResultCreate, TestResultResponse
from app.schemas.progress import VideoProgressCreate, VideoProgressResponse

__all__ = [
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "Token",
    "TokenData",
    "VideoCreate",
    "VideoResponse",
    "VideoCategoryCreate",
    "VideoCategoryResponse",
    "TestCreate",
    "TestResponse",
    "TestQuestionCreate",
    "TestQuestionResponse",
    "TestResultCreate",
    "TestResultResponse",
    "VideoProgressCreate",
    "VideoProgressResponse",
]
