from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app.routes import auth, videos, tests
from datetime import datetime

# Database tables yaratish
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    description="Madinabonu - Ta'lim platformasi backend API",
    debug=settings.DEBUG
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router)
app.include_router(videos.router)
app.include_router(tests.router)

@app.get("/")
def health_check():
    """
    Health check endpoint

    Frontend bu endpoint orqali serverni uyg'otishi mumkin.
    Render sleep mode dan chiqish uchun birinchi request.
    Timeout: 90 sekund tavsiya etiladi.
    """
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.API_VERSION,
        "message": "Madinabonu Backend API ishlamoqda!",
        "timestamp": datetime.utcnow().isoformat(),
        "render_info": {
            "free_plan": True,
            "sleep_after_inactivity": "15 minutes",
            "wake_up_time": "30-60 seconds",
            "recommendation": "Use 90s timeout for first request"
        }
    }

@app.get("/ping")
def ping():
    """
    Ping endpoint - tez javob qaytaradi

    Keep-alive uchun ishlatiladi.
    Render sleep mode ga o'tishini oldini olish uchun
    har 10 daqiqada ping qilish tavsiya etiladi.
    """
    return {
        "pong": True,
        "timestamp": datetime.utcnow().isoformat(),
        "message": "Server active"
    }

@app.get("/api/info")
def api_info():
    """API ma'lumotlari"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.API_VERSION,
        "endpoints": {
            "health": "/",
            "ping": "/ping",
            "auth": "/auth",
            "videos": "/videos",
            "tests": "/tests",
            "docs": "/docs",
            "redoc": "/redoc"
        },
        "features": [
            "JWT Authentication",
            "Role-based Access Control (superadmin, admin, teacher, client)",
            "Video Courses Management",
            "Interactive Tests & Quizzes",
            "Progress Tracking",
            "AWS S3 Integration",
            "Sleep-aware timeout handling"
        ],
        "deployment": {
            "platform": "Render.com",
            "plan": "Free",
            "cold_start": "30-60s",
            "recommended_timeout": "90s"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
