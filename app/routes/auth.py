from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.models.user import User
from app.models.enums import UserRole
from app.models.oauth import OAuthAccount, OAuthProvider
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.schemas.oauth import OAuthLoginRequest, TokenResponse
from app.utils import hash_password, verify_password, create_access_token, create_refresh_token
from app.dependencies import get_current_user, require_admin, require_superadmin
from app.config import settings
from app.oauth_utils import verify_google_token, verify_apple_token, generate_username_from_email

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

# ============ OAUTH LOGIN (Google & Apple) ============

@router.post("/oauth/login", response_model=TokenResponse)
async def oauth_login(oauth_request: OAuthLoginRequest, db: Session = Depends(get_db)):
    """
    OAuth (Google/Apple) orqali login

    **Public endpoint** - Google yoki Apple orqali ro'yxatdan o'tish/kirish.

    - **provider**: "google" yoki "apple"
    - **id_token**: OAuth provider dan olingan ID token
    - **access_token**: Google uchun access token (ixtiyoriy)

    **Flow:**
    1. Mobile app Google/Apple SDK orqali user login qiladi
    2. SDK ID token qaytaradi
    3. Mobile bu endpointga ID token yuboradi
    4. Backend token verify qilib user yaratadi/topib JWT token qaytaradi
    """

    provider = oauth_request.provider.lower()

    if provider not in ["google", "apple"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Noto'g'ri provider. 'google' yoki 'apple' bo'lishi kerak."
        )

    # Token verification
    user_info = None

    if provider == "google":
        user_info = await verify_google_token(
            oauth_request.id_token,
            oauth_request.access_token
        )
    elif provider == "apple":
        user_info = await verify_apple_token(oauth_request.id_token)

    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="OAuth token verification failed"
        )

    # OAuth account mavjudligini tekshirish
    oauth_account = db.query(OAuthAccount).filter(
        OAuthAccount.provider_user_id == user_info.provider_user_id,
        OAuthAccount.provider == OAuthProvider[provider.upper()]
    ).first()

    if oauth_account:
        # User allaqachon mavjud - login
        user = oauth_account.user

        # OAuth account ma'lumotlarini yangilash
        if user_info.email:
            oauth_account.email = user_info.email
        if user_info.full_name:
            oauth_account.full_name = user_info.full_name
        if user_info.picture:
            oauth_account.picture = user_info.picture

        db.commit()
    else:
        # Yangi user yaratish
        # Email orqali mavjud userni topishga harakat
        user = None
        if user_info.email:
            user = db.query(User).filter(User.email == user_info.email).first()

        if user:
            # Email bo'yicha user topildi - OAuth account biriktirish
            pass
        else:
            # Yangi user yaratish
            username = generate_username_from_email(
                user_info.email or "",
                provider
            )

            # Username unique bo'lishi kerak
            counter = 1
            original_username = username
            while db.query(User).filter(User.username == username).first():
                username = f"{original_username}{counter}"
                counter += 1

            user = User(
                username=username,
                email=user_info.email,
                full_name=user_info.full_name,
                hashed_password=None,  # OAuth uchun parol yo'q
                role=UserRole.CLIENT,
                is_active=True
            )

            db.add(user)
            db.commit()
            db.refresh(user)

        # OAuth account yaratish
        new_oauth_account = OAuthAccount(
            user_id=user.id,
            provider=OAuthProvider[provider.upper()],
            provider_user_id=user_info.provider_user_id,
            email=user_info.email,
            full_name=user_info.full_name,
            picture=user_info.picture
        )

        db.add(new_oauth_account)
        db.commit()

    # Token yaratish
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role.value}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username, "user_id": user.id}
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user_id=user.id,
        username=user.username,
        email=user.email,
        role=user.role.value
    )
