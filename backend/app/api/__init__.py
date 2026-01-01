"""API router initialization."""

from fastapi import APIRouter
from .health import router as health_router
from .tryon import router as tryon_router
from .api_keys import router as api_keys_router

api_router = APIRouter()

# Include all routers
api_router.include_router(health_router)
api_router.include_router(tryon_router)
api_router.include_router(api_keys_router)
