"""Image processing utilities."""

import os
from PIL import Image
import numpy as np
from typing import Tuple, Optional
import io


class ImageProcessor:
    """Image processing utilities for virtual try-on."""
    
    @staticmethod
    def validate_image(image_bytes: bytes) -> bool:
        """Validate that the input is a valid image."""
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img.verify()
            return True
        except Exception:
            return False
    
    @staticmethod
    def resize_image(image: Image.Image, max_size: Tuple[int, int] = (768, 1024)) -> Image.Image:
        """Resize image while maintaining aspect ratio."""
        img = image.copy()
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        return img
    
    @staticmethod
    def save_uploaded_image(image_bytes: bytes, save_path: str) -> str:
        """Save uploaded image to disk."""
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert RGBA to RGB if necessary
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        img.save(save_path, 'JPEG', quality=95)
        return save_path
    
    @staticmethod
    def load_image(image_path: str) -> Optional[Image.Image]:
        """Load image from disk."""
        try:
            return Image.open(image_path)
        except Exception:
            return None
    
    @staticmethod
    def prepare_for_model(image: Image.Image) -> np.ndarray:
        """Prepare image for model input."""
        # Resize to model input size
        img_resized = image.resize((768, 1024), Image.Resampling.LANCZOS)
        
        # Convert to numpy array and normalize
        img_array = np.array(img_resized).astype(np.float32) / 255.0
        
        # Transpose to CHW format (channels first)
        img_array = np.transpose(img_array, (2, 0, 1))
        
        return img_array
