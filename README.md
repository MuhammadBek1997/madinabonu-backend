# Madinabonu Backend API

Web va mobil platforma uchun backend API (FastAPI + PostgreSQL)

## Funksiyalar

- **User Management** - Foydalanuvchilar ro'yxatdan o'tishi va login
- **Video Courses** - Video kurslar va darsliklar
- **Tests & Quizzes** - Interaktiv testlar va baholash
- **Progress Tracking** - Foydalanuvchi progressini kuzatish
- **Categories & Subjects** - Kurs kategoriyalari va mavzular

## Texnologiyalar

- FastAPI 0.115.6
- PostgreSQL (SQLAlchemy)
- JWT Authentication
- AWS S3 (video va rasmlar uchun)
- Python 3.12

## O'rnatish

```bash
pip install -r requirements.txt
```

## Ishga tushirish

```bash
uvicorn app.main:app --reload
```

## API Documentation

Ishga tushgandan keyin: http://localhost:8000/docs
