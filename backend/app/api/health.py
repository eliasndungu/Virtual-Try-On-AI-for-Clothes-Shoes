"""Health check and system info endpoints."""

from fastapi import APIRouter

from ..models.schemas import HealthResponse
from ..core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        supported_poses=settings.SUPPORTED_POSES
    )


@router.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": settings.DESCRIPTION,
        "docs_url": "/docs",
        "api_v1": settings.API_V1_STR
    }
