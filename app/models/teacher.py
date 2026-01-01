from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Teacher(Base):
    """
    O'qituvchi modeli

    O'qituvchilar platformada video darslar yuklaydi va
    o'quvchilarga ta'lim beradi.
    """
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    experience_years = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    total_students = Column(Integer, default=0)
    total_videos = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="teacher_profile")
    videos = relationship("Video", back_populates="teacher")
    subjects = relationship("TeacherSubject", back_populates="teacher")

    def __repr__(self):
        return f"<Teacher {self.full_name}>"