from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum

class OAuthProvider(str, Enum):
    """OAuth provider turlari"""
    GOOGLE = "google"
    APPLE = "apple"

class OAuthAccount(Base):
    """
    OAuth hisoblar (Google, Apple)

    User bir nechta OAuth provider orqali login qilishi mumkin.
    """
    __tablename__ = "oauth_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(SQLEnum(OAuthProvider), nullable=False)
    provider_user_id = Column(String(255), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=True)
    picture = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="oauth_accounts")

    def __repr__(self):
        return f"<OAuthAccount {self.provider.value} - {self.email}>"