from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class VideoCategory(Base):
    """Video kategoriyalari"""
    __tablename__ = "video_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(255), nullable=True)
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    videos = relationship("Video", back_populates="category")

    def __repr__(self):
        return f"<VideoCategory {self.name}>"

class Video(Base):
    """Video darsliklar"""
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    video_url = Column(String(500), nullable=False)  # S3 URL yoki YouTube URL
    thumbnail_url = Column(String(500), nullable=True)
    duration = Column(Integer, nullable=True)  # soniyalarda
    category_id = Column(Integer, ForeignKey("video_categories.id"), nullable=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)
    is_published = Column(Boolean, default=True)
    order = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    category = relationship("VideoCategory", back_populates="videos")
    subject = relationship("Subject", back_populates="videos")
    teacher = relationship("Teacher", back_populates="videos")

    def __repr__(self):
        return f"<Video {self.title}>"
