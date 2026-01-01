"""Test configuration and fixtures."""

import pytest
import os
from PIL import Image
import io


@pytest.fixture
def sample_person_image():
    """Create a sample person image for testing."""
    img = Image.new('RGB', (512, 768), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


@pytest.fixture
def sample_garment_image():
    """Create a sample garment image for testing."""
    img = Image.new('RGB', (512, 512), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


@pytest.fixture
def test_upload_dir(tmp_path):
    """Create temporary upload directory for testing."""
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    (upload_dir / "persons").mkdir()
    (upload_dir / "garments").mkdir()
    (upload_dir / "results").mkdir()
    return str(upload_dir)
