from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Subject(Base):
    """
    Fan/Kurs modeli

    Platformadagi barcha fanlar (Matematika, Fizika, Ingliz tili, va hokazo)
    """
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    icon_url = Column(String(500), nullable=True)
    order = Column(Integer, default=0)  # Tartib raqami ko'rsatish uchun
    is_active = Column(Integer, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    teachers = relationship("TeacherSubject", back_populates="subject")
    videos = relationship("Video", back_populates="subject")

    def __repr__(self):
        return f"<Subject {self.name}>"


class TeacherSubject(Base):
    """
    O'qituvchi va Fan orasidagi Many-to-Many bog'lanish

    Bir o'qituvchi bir nechta fanni o'qitishi mumkin,
    bir fanni bir nechta o'qituvchi o'qitishi mumkin.
    """
    __tablename__ = "teacher_subjects"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    teacher = relationship("Teacher", back_populates="subjects")
    subject = relationship("Subject", back_populates="teachers")

    def __repr__(self):
        return f"<TeacherSubject teacher_id={self.teacher_id} subject_id={self.subject_id}>"