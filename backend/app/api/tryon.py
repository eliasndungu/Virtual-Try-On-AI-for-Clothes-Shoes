"""API endpoints for virtual try-on system."""

import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import shutil

from ..models import (
    TryOnRequestSchema,
    TryOnResponse,
    TryOnRequestDetail,
    PoseType,
    TryOnStatus,
)
from ..models.database import TryOnRequest as TryOnRequestDB
from ..services import get_db, VirtualTryOnService
from ..utils import ImageProcessor, generate_filename
from ..core.config import settings

router = APIRouter(prefix="/tryon", tags=["Virtual Try-On"])

tryon_service = VirtualTryOnService()
image_processor = ImageProcessor()


async def process_tryon_background(
    request_id: int,
    person_image_path: str,
    garment_image_path: str,
    pose: str,
    output_path: str,
    db_session: AsyncSession
):
    """Background task to process virtual try-on."""
    # Update status to processing
    result = await db_session.execute(
        select(TryOnRequestDB).where(TryOnRequestDB.id == request_id)
    )
    request_obj = result.scalar_one_or_none()
    
    if request_obj:
        request_obj.status = "processing"
        await db_session.commit()
    
    # Process the try-on
    success, error_msg, proc_time = tryon_service.process_tryon(
        person_image_path,
        garment_image_path,
        pose,
        output_path
    )
    
    # Update request with results
    if request_obj:
        request_obj.status = "completed" if success else "failed"
        request_obj.result_image_path = output_path if success else None
        request_obj.error_message = error_msg
        request_obj.processing_time = proc_time
        await db_session.commit()


@router.post("/", response_model=TryOnResponse)
async def create_tryon_request(
    background_tasks: BackgroundTasks,
    person_image: UploadFile = File(..., description="Image of the person"),
    garment_image: UploadFile = File(..., description="Image of the garment"),
    pose: PoseType = Form(default=PoseType.FRONT, description="Pose type"),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new virtual try-on request.
    
    Upload a person image and a garment image, and receive a try-on result.
    Processing happens in the background, use the request_id to check status.
    """
    # Validate image types
    if person_image.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid person image type")
    if garment_image.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid garment image type")
    
    # Read and validate images
    person_bytes = await person_image.read()
    garment_bytes = await garment_image.read()
    
    if len(person_bytes) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="Person image too large")
    if len(garment_bytes) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="Garment image too large")
    
    if not image_processor.validate_image(person_bytes):
        raise HTTPException(status_code=400, detail="Invalid person image")
    if not image_processor.validate_image(garment_bytes):
        raise HTTPException(status_code=400, detail="Invalid garment image")
    
    # Save uploaded images
    person_filename = generate_filename("person", "jpg")
    garment_filename = generate_filename("garment", "jpg")
    result_filename = generate_filename("result", "jpg")
    
    person_path = os.path.join(settings.UPLOAD_DIR, "persons", person_filename)
    garment_path = os.path.join(settings.UPLOAD_DIR, "garments", garment_filename)
    result_path = os.path.join(settings.UPLOAD_DIR, "results", result_filename)
    
    image_processor.save_uploaded_image(person_bytes, person_path)
    image_processor.save_uploaded_image(garment_bytes, garment_path)
    
    # Create database record
    db_request = TryOnRequestDB(
        user_image_path=person_path,
        garment_image_path=garment_path,
        pose=pose.value,
        status="pending"
    )
    
    db.add(db_request)
    await db.commit()
    await db.refresh(db_request)
    
    # Schedule background processing
    background_tasks.add_task(
        process_tryon_background,
        db_request.id,
        person_path,
        garment_path,
        pose.value,
        result_path,
        db
    )
    
    return TryOnResponse(
        request_id=db_request.id,
        status=TryOnStatus.PENDING,
        message="Try-on request created successfully. Processing in background.",
        created_at=db_request.created_at
    )


@router.get("/{request_id}", response_model=TryOnRequestDetail)
async def get_tryon_request(
    request_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get details of a specific try-on request."""
    result = await db.execute(
        select(TryOnRequestDB).where(TryOnRequestDB.id == request_id)
    )
    request_obj = result.scalar_one_or_none()
    
    if not request_obj:
        raise HTTPException(status_code=404, detail="Try-on request not found")
    
    return TryOnRequestDetail.model_validate(request_obj)


@router.get("/", response_model=List[TryOnRequestDetail])
async def list_tryon_requests(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """List all try-on requests."""
    result = await db.execute(
        select(TryOnRequestDB)
        .order_by(TryOnRequestDB.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    requests = result.scalars().all()
    
    return [TryOnRequestDetail.model_validate(req) for req in requests]
