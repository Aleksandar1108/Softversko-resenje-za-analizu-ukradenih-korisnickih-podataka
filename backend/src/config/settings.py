"""Application settings."""
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "Breach Analyzer"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    
    # Database
    # Default to SQLite for easier testing (no setup required)
    # For production, use PostgreSQL: postgresql+asyncpg://user:password@localhost:5432/breach_analyzer
    DATABASE_URL: str = "sqlite+aiosqlite:///./breach_analyzer.db"
    
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # HIBP API
    HIBP_API_KEY: str = ""
    
    # SMTP
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    
    # ML Models
    ML_MODELS_PATH: Path = Path("models")
    
    # Redis (for caching and queues)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
