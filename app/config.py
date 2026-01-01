import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings"""

    # App Info
    APP_NAME: str = Field(default="Madinabonu")
    API_VERSION: str = Field(default="v1")
    DEBUG: bool = Field(default=False)

    # Database
    DATABASE_URL: str = Field(default="postgresql://localhost/madinabonu")

    # JWT
    SECRET_KEY: str = Field(default="change-this-secret-key")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24 * 7)  # 7 kun
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24 * 30)  # 30 kun

    # AWS S3
    AWS_ACCESS_KEY_ID: str = Field(default="")
    AWS_SECRET_KEY: str = Field(default="")
    S3_REGION: str = Field(default="us-east-1")
    S3_BUCKET_NAME: str = Field(default="")

    # CORS
    CORS_ORIGINS: str = Field(default="http://localhost:3000")

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def cors_origins_list(self) -> list:
        """CORS origins ni list ga aylantirish"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

settings = Settings()
