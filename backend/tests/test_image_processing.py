"""Tests for image processing utilities."""

import pytest
from PIL import Image
import io

from app.utils.image_processing import ImageProcessor


class TestImageProcessor:
    """Test ImageProcessor class."""
    
    def test_validate_valid_image(self, sample_person_image):
        """Test validation of a valid image."""
        assert ImageProcessor.validate_image(sample_person_image.read())
    
    def test_validate_invalid_image(self):
        """Test validation of invalid image data."""
        assert not ImageProcessor.validate_image(b"not an image")
    
    def test_resize_image(self):
        """Test image resizing."""
        img = Image.new('RGB', (1000, 1500), color='blue')
        resized = ImageProcessor.resize_image(img, max_size=(500, 750))
        
        assert resized.size[0] <= 500
        assert resized.size[1] <= 750
    
    def test_save_and_load_image(self, sample_person_image, test_upload_dir):
        """Test saving and loading images."""
        save_path = f"{test_upload_dir}/test_image.jpg"
        
        # Save image
        ImageProcessor.save_uploaded_image(sample_person_image.read(), save_path)
        
        # Load image
        loaded_img = ImageProcessor.load_image(save_path)
        
        assert loaded_img is not None
        assert loaded_img.mode == 'RGB'
    
    def test_prepare_for_model(self):
        """Test image preparation for model input."""
        img = Image.new('RGB', (512, 768), color='green')
        prepared = ImageProcessor.prepare_for_model(img)
        
        # Check shape is CHW format
        assert prepared.shape == (3, 1024, 768)
        
        # Check normalization
        assert prepared.min() >= 0
        assert prepared.max() <= 1
