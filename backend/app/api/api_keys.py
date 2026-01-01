"""API key management endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ..models import APIKeyCreate, APIKeyResponse
from ..models.database import APIKey
from ..services import get_db
from ..utils import generate_api_key

router = APIRouter(prefix="/api-keys", tags=["API Keys"])


@router.post("/", response_model=APIKeyResponse)
async def create_api_key(
    api_key_data: APIKeyCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new API key for integration."""
    key = generate_api_key()
    
    db_api_key = APIKey(
        key=key,
        name=api_key_data.name,
        is_active=True
    )
    
    db.add(db_api_key)
    await db.commit()
    await db.refresh(db_api_key)
    
    return APIKeyResponse.model_validate(db_api_key)


@router.get("/", response_model=List[APIKeyResponse])
async def list_api_keys(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """List all API keys."""
    result = await db.execute(
        select(APIKey)
        .order_by(APIKey.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    api_keys = result.scalars().all()
    
    return [APIKeyResponse.model_validate(key) for key in api_keys]


@router.delete("/{key_id}")
async def delete_api_key(
    key_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Deactivate an API key."""
    result = await db.execute(
        select(APIKey).where(APIKey.id == key_id)
    )
    api_key = result.scalar_one_or_none()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    api_key.is_active = False
    await db.commit()
    
    return {"message": "API key deactivated successfully"}
