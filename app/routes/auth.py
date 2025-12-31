from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.models.user import User
from app.models.enums import UserRole
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.utils import hash_password, verify_password, create_access_token, create_refresh_token
from app.dependencies import get_current_user, require_admin, require_superadmin
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Yangi foydalanuvchi ro'yxatdan o'tkazish

    - **username**: Noyob username (3-100 belgi)
    - **password**: Parol (minimum 6 belgi)
    - **email**: Email (ixtiyoriy)
    - **full_name**: To'liq ism (ixtiyoriy)
    - **role**: client (default), teacher, admin, superadmin

    **Eslatma:** Admin va superadmin rollari faqat mavjud admin tomonidan berilishi mumkin
    """

    # Username mavjudligini tekshirish
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu username allaqachon ro'yxatdan o'tgan"
        )

    # Email mavjudligini tekshirish
    if user_data.email:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bu email allaqachon ro'yxatdan o'tgan"
            )

    # Parol uzunligini tekshirish
    if len(user_data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parol kamida 6 belgidan iborat bo'lishi kerak"
        )

    # Role tekshirish - oddiy foydalanuvchilar faqat CLIENT bo'lishi mumkin
    # Admin/Teacher/Superadmin yaratish uchun alohida endpoint kerak
    allowed_roles = [UserRole.CLIENT]
    if user_data.role not in allowed_roles:
        user_data.role = UserRole.CLIENT

    # Yangi foydalanuvchi yaratish
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        role=user_data.role,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/register-staff", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_staff(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Admin/Teacher yaratish (faqat admin uchun)

    Faqat ADMIN yoki SUPERADMIN foydalanuvchilar teacher/admin yaratishi mumkin.
    SUPERADMIN yaratish faqat mavjud SUPERADMIN tomonidan amalga oshiriladi.
    """

    # SUPERADMIN yaratish faqat SUPERADMIN tomonidan
    if user_data.role == UserRole.SUPERADMIN and current_admin.role != UserRole.SUPERADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Faqat superadmin boshqa superadmin yarata oladi"
        )

    # Username mavjudligini tekshirish
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu username allaqachon ro'yxatdan o'tgan"
        )

    # Email mavjudligini tekshirish
    if user_data.email:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bu email allaqachon ro'yxatdan o'tgan"
            )

    # Yangi staff yaratish
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        role=user_data.role,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login - JWT token olish

    - **username**: Username
    - **password**: Parol

    Returns: access_token, refresh_token
    """

    # Foydalanuvchini topish
    user = db.query(User).filter(User.username == user_credentials.username).first()

    # User topilmasa yoki parol noto'g'ri bo'lsa
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username yoki parol noto'g'ri",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Faol emasligini tekshirish
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Foydalanuvchi faol emas"
        )

    # Token yaratish
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id, "role": user.role.value})
    refresh_token = create_refresh_token(data={"sub": user.username, "user_id": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Joriy foydalanuvchi ma'lumotlarini olish

    Requires: Bearer Token
    """
    return current_user

@router.get("/check-role/{role}")
async def check_user_role(role: UserRole, current_user: User = Depends(get_current_user)):
    """
    Foydalanuvchi rolini tekshirish

    Returns: True/False - foydalanuvchining kerakli huquqi bor yoki yo'q
    """
    has_permission = current_user.has_permission(role)

    return {
        "username": current_user.username,
        "current_role": current_user.role.value,
        "required_role": role.value,
        "has_permission": has_permission
    }

@router.get("/users", response_model=list[UserResponse])
async def get_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Barcha foydalanuvchilarni ko'rish

    Faqat ADMIN va SUPERADMIN uchun
    """
    users = db.query(User).all()
    return users

@router.patch("/users/{user_id}/role")
async def change_user_role(
    user_id: int,
    new_role: UserRole,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    Foydalanuvchi rolini o'zgartirish

    Faqat ADMIN va SUPERADMIN uchun.
    SUPERADMIN rolini faqat SUPERADMIN o'zgartira oladi.
    """

    # Foydalanuvchini topish
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foydalanuvchi topilmadi"
        )

    # SUPERADMIN rolini faqat SUPERADMIN o'zgartira oladi
    if new_role == UserRole.SUPERADMIN and current_admin.role != UserRole.SUPERADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Faqat superadmin boshqa foydalanuvchiga superadmin roli bera oladi"
        )

    # Rolini o'zgartirish
    user.role = new_role
    db.commit()
    db.refresh(user)

    return {
        "message": "Foydalanuvchi roli muvaffaqiyatli o'zgartirildi",
        "user_id": user.id,
        "username": user.username,
        "new_role": user.role.value
    }
