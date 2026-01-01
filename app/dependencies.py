from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.user import User
from app.models.enums import UserRole
from app.utils import decode_token

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Joriy foydalanuvchini olish (JWT token orqali)"""
    token = credentials.credentials

    # Token ni decode qilish
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token yaroqsiz yoki muddati tugagan",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Username olish
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token ma'lumotlari noto'g'ri",
        )

    # Foydalanuvchini bazadan topish
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Foydalanuvchi topilmadi",
        )

    # Aktiv emasligini tekshirish
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Foydalanuvchi faol emas",
        )

    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Aktiv foydalanuvchi"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Foydalanuvchi faol emas"
        )
    return current_user

# Role-based dependencies

async def require_superadmin(
    current_user: User = Depends(get_current_user)
) -> User:
    """Faqat SUPERADMIN ruxsat beriladi"""
    if current_user.role != UserRole.SUPERADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Faqat superadmin uchun ruxsat berilgan"
        )
    return current_user

async def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """ADMIN yoki SUPERADMIN ruxsat beriladi"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin huquqlari talab qilinadi"
        )
    return current_user

async def require_teacher(
    current_user: User = Depends(get_current_user)
) -> User:
    """TEACHER, ADMIN yoki SUPERADMIN ruxsat beriladi"""
    if not current_user.is_teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher yoki yuqori huquqlar talab qilinadi"
        )
    return current_user

def require_role(required_role: UserRole):
    """Custom role dependency factory"""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if not current_user.has_permission(required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"{required_role.value} yoki yuqori huquqlar talab qilinadi"
            )
        return current_user
    return role_checker
