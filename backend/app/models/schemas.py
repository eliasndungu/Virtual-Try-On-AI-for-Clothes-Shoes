"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class PoseType(str, Enum):
    """Supported pose types."""
    FRONT = "front"
    SIDE = "side"
    THREE_QUARTER = "three-quarter"


class TryOnStatus(str, Enum):
    """Try-on request status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TryOnRequest(BaseModel):
    """Schema for try-on request."""
    pose: PoseType = Field(default=PoseType.FRONT, description="Pose type for the try-on")
    
    class Config:
        use_enum_values = True


class TryOnResponse(BaseModel):
    """Schema for try-on response."""
    request_id: int
    status: TryOnStatus
    result_image_url: Optional[str] = None
    message: str
    created_at: datetime
    processing_time: Optional[float] = None
    
    class Config:
        from_attributes = True


class TryOnRequestDetail(BaseModel):
    """Detailed try-on request schema."""
    id: int
    user_image_path: str
    garment_image_path: str
    result_image_path: Optional[str]
    pose: str
    status: str
    created_at: datetime
    updated_at: datetime
    error_message: Optional[str]
    processing_time: Optional[float]
    
    class Config:
        from_attributes = True


class APIKeyCreate(BaseModel):
    """Schema for creating API key."""
    name: str = Field(..., description="Name/description for the API key")


class APIKeyResponse(BaseModel):
    """Schema for API key response."""
    id: int
    key: str
    name: str
    is_active: bool
    created_at: datetime
    usage_count: int
    
    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    supported_poses: List[str]
