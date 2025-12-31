from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Test(Base):
    """Test/Quiz"""
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=True)
    category = Column(String(100), nullable=True)
    subject = Column(String(100), nullable=True)
    time_limit = Column(Integer, default=600)  # soniyalarda (default 10 daqiqa)
    passing_score = Column(Integer, default=70)  # foizda
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    questions = relationship("TestQuestion", back_populates="test", cascade="all, delete-orphan")
    results = relationship("TestResult", back_populates="test")

    def __repr__(self):
        return f"<Test {self.title}>"

class TestQuestion(Base):
    """Test savollari"""
    __tablename__ = "test_questions"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # ["A) Variant 1", "B) Variant 2", ...]
    correct_answer = Column(Integer, nullable=False)  # 0, 1, 2, 3 (index)
    image_url = Column(String(500), nullable=True)
    explanation = Column(Text, nullable=True)
    order = Column(Integer, default=0)

    # Relationships
    test = relationship("Test", back_populates="questions")

    def __repr__(self):
        return f"<TestQuestion {self.id}>"

class TestResult(Base):
    """Test natijalari"""
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    score = Column(Integer, nullable=False)  # to'g'ri javoblar soni
    total_questions = Column(Integer, nullable=False)
    percentage = Column(Integer, nullable=False)  # foizda
    time_spent = Column(Integer, nullable=True)  # soniyalarda
    passed = Column(Boolean, default=False)
    answers = Column(JSON, nullable=True)  # foydalanuvchi javoblari
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    test = relationship("Test", back_populates="results")

    def __repr__(self):
        return f"<TestResult user={self.user_id} test={self.test_id} score={self.score}>"
