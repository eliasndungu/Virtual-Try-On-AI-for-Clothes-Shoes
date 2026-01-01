#!/usr/bin/env python
"""Quick test script to verify the API is working."""

import requests
import sys
from PIL import Image
import io

def test_health():
    """Test health endpoint."""
    print("Testing /health endpoint...")
    response = requests.get("http://localhost:8000/api/v1/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Health check passed: {data}")
        return True
    else:
        print(f"✗ Health check failed: {response.status_code}")
        return False

def test_root():
    """Test root endpoint."""
    print("\nTesting / endpoint...")
    response = requests.get("http://localhost:8000/")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Root endpoint passed: {data.get('name')}")
        return True
    else:
        print(f"✗ Root endpoint failed: {response.status_code}")
        return False

def create_test_image():
    """Create a test image in memory."""
    img = Image.new('RGB', (512, 768), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

def test_tryon():
    """Test try-on endpoint."""
    print("\nTesting /tryon endpoint...")
    
    # Create test images
    person_img = create_test_image()
    garment_img = create_test_image()
    
    files = {
        'person_image': ('person.jpg', person_img, 'image/jpeg'),
        'garment_image': ('garment.jpg', garment_img, 'image/jpeg')
    }
    data = {'pose': 'front'}
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/tryon/",
            files=files,
            data=data
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Try-on request created: ID {data.get('request_id')}")
            return True
        else:
            print(f"✗ Try-on request failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to API. Make sure the server is running.")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Virtual Try-On API Quick Test")
    print("=" * 60)
    
    results = []
    results.append(test_health())
    results.append(test_root())
    results.append(test_tryon())
    
    print("\n" + "=" * 60)
    if all(results):
        print("✓ All tests passed!")
        print("=" * 60)
        return 0
    else:
        print("✗ Some tests failed")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
