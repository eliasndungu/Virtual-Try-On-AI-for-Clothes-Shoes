"""Database models for virtual try-on system."""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class TryOnRequest(Base):
    """Model for storing try-on requests."""
    
    __tablename__ = "tryon_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_image_path = Column(String, nullable=False)
    garment_image_path = Column(String, nullable=False)
    result_image_path = Column(String, nullable=True)
    pose = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=func.now())
    error_message = Column(String, nullable=True)
    processing_time = Column(Float, nullable=True)


class APIKey(Base):
    """Model for API key management."""
    
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
    last_used_at = Column(DateTime, nullable=True)
    usage_count = Column(Integer, default=0)
