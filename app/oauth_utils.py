"""
OAuth utility functions for Google and Apple Sign-In
"""

from typing import Optional
from jose import jwt, JWTError
import requests
from app.schemas.oauth import OAuthUserInfo

# Google OAuth
GOOGLE_OAUTH_URL = "https://oauth2.googleapis.com/tokeninfo"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

# Apple OAuth
APPLE_JWKS_URL = "https://appleid.apple.com/auth/keys"


async def verify_google_token(id_token: str, access_token: Optional[str] = None) -> Optional[OAuthUserInfo]:
    """
    Google ID token ni verify qilish

    Returns: OAuthUserInfo yoki None
    """
    try:
        # ID token verification
        response = requests.get(
            GOOGLE_OAUTH_URL,
            params={"id_token": id_token},
            timeout=5
        )

        if response.status_code != 200:
            print(f"Google token verification failed: {response.text}")
            return None

        token_info = response.json()

        # Token ma'lumotlarini olish
        user_id = token_info.get("sub")  # Google user ID
        email = token_info.get("email")
        email_verified = token_info.get("email_verified", False)

        if not user_id:
            return None

        # User info olish (agar access_token berilgan bo'lsa)
        full_name = None
        picture = None
        given_name = None
        family_name = None

        if access_token:
            try:
                userinfo_response = requests.get(
                    GOOGLE_USERINFO_URL,
                    headers={"Authorization": f"Bearer {access_token}"},
                    timeout=5
                )

                if userinfo_response.status_code == 200:
                    userinfo = userinfo_response.json()
                    full_name = userinfo.get("name")
                    picture = userinfo.get("picture")
                    given_name = userinfo.get("given_name")
                    family_name = userinfo.get("family_name")
            except Exception as e:
                print(f"Error fetching Google userinfo: {e}")

        # Agar full_name yo'q bo'lsa, token_info dan olishga harakat
        if not full_name:
            full_name = token_info.get("name")

        return OAuthUserInfo(
            provider_user_id=user_id,
            email=email if email_verified else None,
            full_name=full_name,
            picture=picture,
            given_name=given_name,
            family_name=family_name
        )

    except Exception as e:
        print(f"Google token verification error: {e}")
        return None


async def verify_apple_token(id_token: str) -> Optional[OAuthUserInfo]:
    """
    Apple ID token ni verify qilish

    Apple Sign In JWT token ni decode qilib user ma'lumotlarini olish.
    Production da Apple public key bilan verify qilish kerak.

    Returns: OAuthUserInfo yoki None
    """
    try:
        # Apple token ni decode qilish (verify=False - development uchun)
        # Production da verify=True qilib Apple public key ishlatish kerak
        decoded = jwt.decode(
            id_token,
            options={"verify_signature": False}  # ⚠️ Production da True qiling!
        )

        user_id = decoded.get("sub")  # Apple user ID
        email = decoded.get("email")
        email_verified = decoded.get("email_verified", False)

        if not user_id:
            return None

        # Apple faqat birinchi marta email beradi
        # Keyingi loginlarda faqat user_id qaytaradi

        return OAuthUserInfo(
            provider_user_id=user_id,
            email=email if email_verified else None,
            full_name=None,  # Apple full name bermaydi
            picture=None,
            given_name=None,
            family_name=None
        )

    except JWTError as e:
        print(f"Apple token decode error: {e}")
        return None
    except Exception as e:
        print(f"Apple token verification error: {e}")
        return None


def generate_username_from_email(email: str, provider: str) -> str:
    """
    Email dan unique username yaratish

    Example: john.doe@gmail.com -> john_doe_google
    """
    if not email:
        import uuid
        return f"{provider}_{uuid.uuid4().hex[:8]}"

    # Email dan username qismini olish
    local_part = email.split("@")[0]

    # Belgisizlarni _ ga almashtirish
    username = local_part.replace(".", "_").replace("-", "_").lower()

    # Provider qo'shish
    username = f"{username}_{provider}"

    return username