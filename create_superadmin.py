"""
Superadmin yaratish scripti

Bu script birinchi marta ishga tushirilganda superadmin hisobini yaratadi.
Email: allayevmuhammad4@gmail.com
Username: superadmin
Password: superadminpass
"""

from app.database import SessionLocal
from app.models.user import User
from app.models.enums import UserRole
from app.utils import hash_password

def create_superadmin():
    db = SessionLocal()

    try:
        # Superadmin mavjudligini tekshirish
        existing_superadmin = db.query(User).filter(
            User.email == "allayevmuhammad4@gmail.com"
        ).first()

        if existing_superadmin:
            print("❌ Superadmin allaqachon mavjud!")
            print(f"   Username: {existing_superadmin.username}")
            print(f"   Email: {existing_superadmin.email}")
            print(f"   Role: {existing_superadmin.role.value}")
            return

        # Yangi superadmin yaratish
        superadmin = User(
            username="superadmin",
            email="allayevmuhammad4@gmail.com",
            full_name="Muhammad Allayev",
            hashed_password=hash_password("superadminpass"),
            role=UserRole.SUPERADMIN,
            is_active=True
        )

        db.add(superadmin)
        db.commit()
        db.refresh(superadmin)

        print("✅ Superadmin muvaffaqiyatli yaratildi!")
        print(f"   ID: {superadmin.id}")
        print(f"   Username: {superadmin.username}")
        print(f"   Email: {superadmin.email}")
        print(f"   Password: superadminpass")
        print(f"   Role: {superadmin.role.value}")
        print("\n🔐 Login uchun:")
        print(f"   POST http://localhost:8000/auth/login")
        print(f"   Body: {{\"username\": \"superadmin\", \"password\": \"superadminpass\"}}")

    except Exception as e:
        print(f"❌ Xatolik yuz berdi: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Superadmin yaratish jarayoni boshlandi...")
    print("-" * 50)
    create_superadmin()
    print("-" * 50)