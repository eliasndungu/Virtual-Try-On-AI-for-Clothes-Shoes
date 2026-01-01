"""Tests for virtual try-on service."""

import pytest
from PIL import Image
import os

from app.services.tryon_service import VirtualTryOnService
from app.utils.image_processing import ImageProcessor


class TestVirtualTryOnService:
    """Test VirtualTryOnService class."""
    
    def test_process_tryon(self, sample_person_image, sample_garment_image, test_upload_dir):
        """Test virtual try-on processing."""
        service = VirtualTryOnService()
        
        # Save sample images
        person_path = f"{test_upload_dir}/persons/person.jpg"
        garment_path = f"{test_upload_dir}/garments/garment.jpg"
        output_path = f"{test_upload_dir}/results/result.jpg"
        
        ImageProcessor.save_uploaded_image(sample_person_image.read(), person_path)
        ImageProcessor.save_uploaded_image(sample_garment_image.read(), garment_path)
        
        # Process try-on
        success, error_msg, proc_time = service.process_tryon(
            person_path,
            garment_path,
            "front",
            output_path
        )
        
        assert success is True
        assert error_msg is None
        assert proc_time is not None
        assert os.path.exists(output_path)
    
    def test_process_tryon_invalid_pose(self, sample_person_image, sample_garment_image, test_upload_dir):
        """Test try-on with invalid pose."""
        service = VirtualTryOnService()
        
        person_path = f"{test_upload_dir}/persons/person.jpg"
        garment_path = f"{test_upload_dir}/garments/garment.jpg"
        output_path = f"{test_upload_dir}/results/result.jpg"
        
        ImageProcessor.save_uploaded_image(sample_person_image.read(), person_path)
        ImageProcessor.save_uploaded_image(sample_garment_image.read(), garment_path)
        
        success, error_msg, proc_time = service.process_tryon(
            person_path,
            garment_path,
            "invalid_pose",
            output_path
        )
        
        assert success is False
        assert "Unsupported pose" in error_msg
    
    def test_validate_person_pose(self):
        """Test person pose validation."""
        service = VirtualTryOnService()
        
        # For MVP, this always returns True
        assert service.validate_person_pose("dummy_path.jpg", "front") is True
