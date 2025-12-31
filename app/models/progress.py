from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.sql import func
from app.database import Base

class VideoProgress(Base):
    """Foydalanuvchi video progressi"""
    __tablename__ = "video_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    progress_seconds = Column(Integer, default=0)  # qayerda to'xtagani
    completed = Column(Boolean, default=False)
    completion_percentage = Column(Float, default=0.0)
    last_watched = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<VideoProgress user={self.user_id} video={self.video_id}>"
