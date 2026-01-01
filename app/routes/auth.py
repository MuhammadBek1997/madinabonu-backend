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

# ============ CLIENT REGISTRATION (Public) ============

@router.post("/register/client", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_client(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    CLIENT (o'quvchi) ro'yxatdan o'tish

    **Public endpoint** - har kim erkin ro'yxatdan o'tishi mumkin.
    Avtomatik CLIENT roli beriladi.

    - **username**: Noyob username
    - **password**: Parol (minimum 6 belgi)
    - **email**: Email (ixtiyoriy)
    - **full_name**: To'liq ism (ixtiyoriy)
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

    # Yangi CLIENT yaratish
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        role=UserRole.CLIENT,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# ============ TEACHER REGISTRATION (Admin+) ============

@router.post("/register/teacher", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_teacher(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    TEACHER yaratish

    **Faqat ADMIN va SUPERADMIN uchun.**
    Yangi o'qituvchi hisobini yaratish.
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

    # Yangi TEACHER yaratish
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        role=UserRole.TEACHER,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# ============ ADMIN REGISTRATION (Admin+) ============

@router.post("/register/admin", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_admin(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    """
    ADMIN yaratish

    **Faqat ADMIN va SUPERADMIN uchun.**
    Yangi administrator hisobini yaratish.
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

    # Yangi ADMIN yaratish
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        role=UserRole.ADMIN,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# ============ SUPERADMIN REGISTRATION (Superadmin only) ============

@router.post("/register/superadmin", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_superadmin(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_superadmin: User = Depends(require_superadmin)
):
    """
    SUPERADMIN yaratish

    **Faqat SUPERADMIN uchun.**
    Yangi super administrator hisobini yaratish.
    Eng yuqori xavfsizlik darajasi.
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

    # Yangi SUPERADMIN yaratish
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        role=UserRole.SUPERADMIN,
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
