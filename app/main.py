from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app.routes import auth, videos, tests

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
    allow_origins=settings.CORS_ORIGINS,
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
    """Health check endpoint"""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.API_VERSION,
        "message": "Madinabonu Backend API ishlamoqda!"
    }

@app.get("/api/info")
def api_info():
    """API ma'lumotlari"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.API_VERSION,
        "endpoints": {
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
            "AWS S3 Integration"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
