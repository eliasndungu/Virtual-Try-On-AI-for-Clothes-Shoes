"""Application configuration and settings."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Virtual Try-On AI"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "AI-powered virtual try-on system for clothes and shoes"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./virtual_tryon.db"
    
    # Upload Configuration
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/jpg"]
    
    # Model Configuration
    MODEL_WEIGHTS_DIR: str = "./models/weights"
    SUPPORTED_POSES: List[str] = ["front", "side", "three-quarter"]
    
    # Try-On Configuration
    OUTPUT_IMAGE_FORMAT: str = "JPEG"
    OUTPUT_IMAGE_QUALITY: int = 90
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
