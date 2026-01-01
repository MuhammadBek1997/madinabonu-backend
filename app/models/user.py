from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.enums import UserRole

class User(Base):
    """Foydalanuvchi modeli"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=True)  # OAuth uchun ixtiyoriy
    role = Column(SQLEnum(UserRole), default=UserRole.CLIENT, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    teacher_profile = relationship("Teacher", back_populates="user", uselist=False)
    oauth_accounts = relationship("OAuthAccount", back_populates="user")

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"

    @property
    def is_superadmin(self) -> bool:
        return self.role == UserRole.SUPERADMIN

    @property
    def is_admin(self) -> bool:
        return self.role in [UserRole.SUPERADMIN, UserRole.ADMIN]

    @property
    def is_teacher(self) -> bool:
        return self.role in [UserRole.SUPERADMIN, UserRole.ADMIN, UserRole.TEACHER]

    def has_permission(self, required_role: UserRole) -> bool:
        """Role hierarxiyasini tekshirish"""
        role_hierarchy = {
            UserRole.CLIENT: 0,
            UserRole.TEACHER: 1,
            UserRole.ADMIN: 2,
            UserRole.SUPERADMIN: 3,
        }
        return role_hierarchy.get(self.role, 0) >= role_hierarchy.get(required_role, 0)
