# MadinabonuBackend - O'rnatish va Ishlatish Qo'llanmasi

## 📋 Tizim Talablari

- Python 3.12+
- PostgreSQL 14+
- AWS S3 account (rasmlar uchun - ixtiyoriy)

## 🚀 O'rnatish

### 1. Virtual Environment Yaratish

```bash
cd MadinabonuBackend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Dependencies O'rnatish

```bash
pip install -r requirements.txt
```

### 3. Environment Variables Sozlash

`.env` fayl yaratish:

```bash
cp .env.example .env
```

`.env` faylini tahrirlash:

```env
# Database (PostgreSQL)
DATABASE_URL=postgresql://username:password@localhost:5432/madinabonu

# JWT Secret (ixtiyoriy uzun string)
SECRET_KEY=your-very-long-secret-key-here-change-this

# AWS S3 (ixtiyoriy)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_KEY=your-aws-secret-key
S3_REGION=us-east-1
S3_BUCKET_NAME=madinabonu-videos

# CORS (frontend URL)
CORS_ORIGINS=http://localhost:3000,http://localhost:8081

# App
APP_NAME=Madinabonu
DEBUG=True
```

### 4. Database Yaratish

PostgreSQL da yangi database yaratish:

```sql
CREATE DATABASE madinabonu;
```

### 5. Ishga Tushirish

```bash
uvicorn app.main:app --reload
```

Yoki:

```bash
python -m app.main
```

API ishga tushdi: http://localhost:8000

## 📚 API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔐 Rollar va Huquqlar

### 1. **SUPERADMIN** (Eng yuqori huquq)
- Boshqa superadmin yaratish
- Admin va teacher yaratish
- Barcha foydalanuvchilarni boshqarish
- Barcha kontent boshqarish

### 2. **ADMIN**
- Teacher yaratish
- Foydalanuvchilarni boshqarish
- Barcha kontent boshqarish

### 3. **TEACHER**
- Video va test yaratish
- O'z yaratgan kontentni tahrirlash

### 4. **CLIENT** (Oddiy foydalanuvchi)
- Videolarni ko'rish
- Test ishlash
- O'z natijalarini ko'rish

## 🎯 Asosiy Endpointlar

### Authentication

```bash
# Register (oddiy foydalanuvchi)
POST /auth/register
{
  "username": "student1",
  "password": "password123",
  "email": "student@example.com",
  "full_name": "Student Name"
}

# Login
POST /auth/login
{
  "username": "student1",
  "password": "password123"
}

# O'z ma'lumotlarini ko'rish
GET /auth/me
Headers: Authorization: Bearer <token>

# Admin/Teacher yaratish (faqat admin)
POST /auth/register-staff
Headers: Authorization: Bearer <admin-token>
{
  "username": "teacher1",
  "password": "password123",
  "role": "teacher",
  "full_name": "Teacher Name"
}
```

### Videos

```bash
# Videolarni ko'rish
GET /videos?category_id=1&subject=matematika

# Video yaratish (teacher+)
POST /videos
Headers: Authorization: Bearer <teacher-token>
{
  "title": "Algebra 1-dars",
  "description": "Asosiy tushunchalar",
  "video_url": "https://youtube.com/...",
  "category_id": 1,
  "subject": "matematika"
}
```

### Tests

```bash
# Testlarni ko'rish
GET /tests?category=matematika

# Test yaratish (teacher+)
POST /tests
Headers: Authorization: Bearer <teacher-token>
{
  "title": "Algebra test",
  "questions": [
    {
      "question_text": "2 + 2 = ?",
      "options": ["A) 3", "B) 4", "C) 5", "D) 6"],
      "correct_answer": 1
    }
  ]
}

# Test topshirish
POST /tests/submit
Headers: Authorization: Bearer <token>
{
  "test_id": 1,
  "answers": [1, 0, 2, 3],
  "time_spent": 300
}
```

## 🔧 Birinchi Superadmin Yaratish

Database ga birinchi superadmin qo'shish (SQL):

```sql
-- Parol: admin123 (bcrypt hash)
INSERT INTO users (username, email, full_name, hashed_password, role, is_active)
VALUES (
  'superadmin',
  'admin@madinabonu.uz',
  'Super Admin',
  '$2b$12$KIXxLVhW8YQJGvN5Qr6wHu4V5rZ0V2fK9mXW6bY8YvZ1V2fK9mXW6',
  'superadmin',
  true
);
```

Yoki Python script:

```python
from app.models.user import User
from app.models.enums import UserRole
from app.utils import hash_password
from app.database import SessionLocal

db = SessionLocal()

superadmin = User(
    username="superadmin",
    email="admin@madinabonu.uz",
    full_name="Super Admin",
    hashed_password=hash_password("admin123"),
    role=UserRole.SUPERADMIN,
    is_active=True
)

db.add(superadmin)
db.commit()
print("Superadmin yaratildi!")
```

## 🌐 Deploy (Heroku/Koyeb)

1. Git repo yaratish
2. `.env` o'rniga Heroku Config Vars sozlash
3. PostgreSQL addon qo'shish
4. Deploy qilish

```bash
git init
git add .
git commit -m "Initial commit"
heroku create madinabonu-backend
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

## 📱 Frontend Integratsiya

React/React Native:

```javascript
const API_URL = "http://localhost:8000";

// Login
const response = await fetch(`${API_URL}/auth/login`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ username, password })
});
const { access_token } = await response.json();

// Videolarni olish
const videos = await fetch(`${API_URL}/videos`, {
  headers: { "Authorization": `Bearer ${access_token}` }
});
```

## ❓ Savol-Javoblar

**Q: Database xatosi chiqsa?**
A: `.env` dagi `DATABASE_URL` to'g'riligini tekshiring

**Q: CORS xatosi?**
A: `.env` dagi `CORS_ORIGINS` ga frontend URL ni qo'shing

**Q: Token yaroqsiz?**
A: Login qilib yangi token oling

## 📞 Yordam

Muammo bo'lsa: issues section ga yozing yoki email jo'nating.
