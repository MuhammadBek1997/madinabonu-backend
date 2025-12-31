#!/usr/bin/env python3
"""
Render Shell da ishlatish uchun initial setup script

Ishlatish:
python setup_initial_data.py
"""

from app.models.user import User
from app.models.enums import UserRole
from app.models.video import VideoCategory
from app.utils import hash_password
from app.database import SessionLocal, Base, engine

def create_tables():
    """Database tables yaratish"""
    print("📦 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

def create_superadmin():
    """Superadmin yaratish"""
    db = SessionLocal()

    try:
        # Mavjudligini tekshirish
        existing = db.query(User).filter(User.username == "superadmin").first()
        if existing:
            print("⚠️  Superadmin allaqachon mavjud!")
            return

        # Yangi superadmin
        admin = User(
            username="superadmin",
            email="admin@madinabonu.uz",
            full_name="Super Administrator",
            hashed_password=hash_password("admin123"),
            role=UserRole.SUPERADMIN,
            is_active=True
        )

        db.add(admin)
        db.commit()

        print("✅ Superadmin yaratildi!")
        print("   Username: superadmin")
        print("   Password: admin123")
        print("   ⚠️  PRODUCTION da parolni o'zgartiring!")

    except Exception as e:
        print(f"❌ Xatolik: {e}")
        db.rollback()
    finally:
        db.close()

def create_sample_categories():
    """Namuna kategoriyalar yaratish"""
    db = SessionLocal()

    categories = [
        {"name": "Matematika", "description": "Matematika darsliklari", "order": 1},
        {"name": "Fizika", "description": "Fizika darsliklari", "order": 2},
        {"name": "Kimyo", "description": "Kimyo darsliklari", "order": 3},
        {"name": "Ingliz tili", "description": "Ingliz tili darsliklari", "order": 4},
        {"name": "Tarix", "description": "Tarix darsliklari", "order": 5},
    ]

    try:
        for cat_data in categories:
            existing = db.query(VideoCategory).filter(
                VideoCategory.name == cat_data["name"]
            ).first()

            if not existing:
                category = VideoCategory(**cat_data)
                db.add(category)

        db.commit()
        print(f"✅ {len(categories)} ta kategoriya yaratildi!")

    except Exception as e:
        print(f"❌ Kategoriya yaratishda xatolik: {e}")
        db.rollback()
    finally:
        db.close()

def create_test_users():
    """Test foydalanuvchilar yaratish"""
    db = SessionLocal()

    test_users = [
        {
            "username": "admin1",
            "email": "admin@test.com",
            "full_name": "Admin User",
            "password": "admin123",
            "role": UserRole.ADMIN
        },
        {
            "username": "teacher1",
            "email": "teacher@test.com",
            "full_name": "Teacher User",
            "password": "teacher123",
            "role": UserRole.TEACHER
        },
        {
            "username": "student1",
            "email": "student@test.com",
            "full_name": "Student User",
            "password": "student123",
            "role": UserRole.CLIENT
        },
    ]

    try:
        for user_data in test_users:
            existing = db.query(User).filter(
                User.username == user_data["username"]
            ).first()

            if not existing:
                password = user_data.pop("password")
                user = User(
                    **user_data,
                    hashed_password=hash_password(password),
                    is_active=True
                )
                db.add(user)

        db.commit()
        print(f"✅ Test foydalanuvchilar yaratildi!")
        print("   admin1 / admin123")
        print("   teacher1 / teacher123")
        print("   student1 / student123")

    except Exception as e:
        print(f"❌ Foydalanuvchi yaratishda xatolik: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Asosiy setup funksiyasi"""
    print("🚀 Madinabonu Backend - Initial Setup")
    print("=" * 50)

    # 1. Tables yaratish
    create_tables()

    # 2. Superadmin yaratish
    create_superadmin()

    # 3. Kategoriyalar
    create_sample_categories()

    # 4. Test users (ixtiyoriy)
    print("\n📝 Test foydalanuvchilar yaratilsinmi? (y/n): ", end="")
    try:
        choice = input().lower()
        if choice == 'y':
            create_test_users()
    except:
        print("Skipped test users")

    print("\n" + "=" * 50)
    print("✅ Setup yakunlandi!")
    print("\n🌐 API URL: https://your-app.onrender.com")
    print("📚 Swagger: https://your-app.onrender.com/docs")
    print("📖 ReDoc: https://your-app.onrender.com/redoc")

if __name__ == "__main__":
    main()