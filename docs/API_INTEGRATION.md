# API Integration Guide

## Overview

The Virtual Try-On API provides RESTful endpoints for integrating virtual try-on capabilities into your retail systems.

## Base URL

```
http://your-domain:8000/api/v1
```

## Authentication (Future)

Currently, the API is open for MVP testing. In production, you'll use API keys:

```http
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### 1. Health Check

Check if the API is running and get system information.

**Request:**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "supported_poses": ["front", "side", "three-quarter"]
}
```

### 2. Create Try-On Request

Upload person and garment images to create a try-on request.

**Request:**
```http
POST /tryon/
Content-Type: multipart/form-data

person_image: <image file>
garment_image: <image file>
pose: "front" | "side" | "three-quarter" (optional, default: "front")
```

**Response:**
```json
{
  "request_id": 123,
  "status": "pending",
  "message": "Try-on request created successfully. Processing in background.",
  "created_at": "2024-01-01T12:00:00.000Z"
}
```

**Status Codes:**
- `200`: Success
- `400`: Bad request (invalid image, size too large, etc.)
- `500`: Server error

### 3. Get Try-On Status & Result

Poll this endpoint to check the status of your try-on request.

**Request:**
```http
GET /tryon/{request_id}
```

**Response:**
```json
{
  "id": 123,
  "user_image_path": "uploads/persons/abc123.jpg",
  "garment_image_path": "uploads/garments/def456.jpg",
  "result_image_path": "uploads/results/ghi789.jpg",
  "pose": "front",
  "status": "completed",
  "created_at": "2024-01-01T12:00:00.000Z",
  "updated_at": "2024-01-01T12:00:05.000Z",
  "error_message": null,
  "processing_time": 2.5
}
```

**Status Values:**
- `pending`: Request received, waiting to process
- `processing`: Currently processing
- `completed`: Successfully completed, result available
- `failed`: Processing failed, check error_message

### 4. List Try-On Requests

Get a list of all try-on requests.

**Request:**
```http
GET /tryon/?skip=0&limit=10
```

**Query Parameters:**
- `skip`: Number of records to skip (pagination)
- `limit`: Maximum number of records to return

**Response:**
```json
[
  {
    "id": 123,
    "status": "completed",
    "pose": "front",
    "created_at": "2024-01-01T12:00:00.000Z",
    ...
  },
  ...
]
```

### 5. Create API Key

Generate a new API key for integration.

**Request:**
```http
POST /api-keys/
Content-Type: application/json

{
  "name": "My E-commerce Store"
}
```

**Response:**
```json
{
  "id": 1,
  "key": "sk_abcdef123456...",
  "name": "My E-commerce Store",
  "is_active": true,
  "created_at": "2024-01-01T12:00:00.000Z",
  "usage_count": 0
}
```

## Code Examples

### Python

```python
import requests
import time

# 1. Create try-on request
url = "http://localhost:8000/api/v1/tryon/"

with open('person.jpg', 'rb') as person_file, \
     open('shirt.jpg', 'rb') as garment_file:
    
    files = {
        'person_image': person_file,
        'garment_image': garment_file
    }
    data = {'pose': 'front'}
    
    response = requests.post(url, files=files, data=data)
    result = response.json()
    request_id = result['request_id']
    print(f"Request created: {request_id}")

# 2. Poll for result
while True:
    status_response = requests.get(f"{url}{request_id}")
    status = status_response.json()
    
    print(f"Status: {status['status']}")
    
    if status['status'] == 'completed':
        print(f"Result image: http://localhost:8000/{status['result_image_path']}")
        break
    elif status['status'] == 'failed':
        print(f"Error: {status['error_message']}")
        break
    
    time.sleep(2)
```

### JavaScript/Node.js

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

async function createTryOn() {
  const formData = new FormData();
  formData.append('person_image', fs.createReadStream('person.jpg'));
  formData.append('garment_image', fs.createReadStream('shirt.jpg'));
  formData.append('pose', 'front');

  const response = await axios.post(
    'http://localhost:8000/api/v1/tryon/',
    formData,
    { headers: formData.getHeaders() }
  );

  return response.data.request_id;
}

async function pollResult(requestId) {
  while (true) {
    const response = await axios.get(
      `http://localhost:8000/api/v1/tryon/${requestId}`
    );
    
    const status = response.data;
    console.log('Status:', status.status);
    
    if (status.status === 'completed') {
      console.log('Result:', `http://localhost:8000/${status.result_image_path}`);
      break;
    } else if (status.status === 'failed') {
      console.error('Error:', status.error_message);
      break;
    }
    
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}

// Usage
(async () => {
  const requestId = await createTryOn();
  await pollResult(requestId);
})();
```

### cURL

```bash
# Create try-on request
curl -X POST "http://localhost:8000/api/v1/tryon/" \
  -F "person_image=@person.jpg" \
  -F "garment_image=@shirt.jpg" \
  -F "pose=front"

# Get result
curl "http://localhost:8000/api/v1/tryon/1"
```

## Best Practices

### 1. Image Requirements

- **Format**: JPEG or PNG
- **Max size**: 10MB per image
- **Recommended dimensions**: 512x768 to 1024x1536
- **Person image**: Clear, full-body shot in one of the supported poses
- **Garment image**: Clear product photo on white/neutral background

### 2. Polling Strategy

Don't poll too frequently. Recommended approach:

```python
import time

max_attempts = 30
attempt = 0
delay = 2  # seconds

while attempt < max_attempts:
    status = get_status(request_id)
    
    if status in ['completed', 'failed']:
        break
    
    time.sleep(delay)
    attempt += 1
```

### 3. Error Handling

Always handle errors gracefully:

```python
try:
    response = requests.post(url, files=files)
    response.raise_for_status()
    result = response.json()
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
except ValueError as e:
    print(f"Invalid JSON response: {e}")
```

### 4. Image Optimization

Pre-process images before uploading:

```python
from PIL import Image

def optimize_image(image_path, max_size=(768, 1024)):
    img = Image.open(image_path)
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    optimized_path = 'optimized_' + image_path
    img.save(optimized_path, 'JPEG', quality=90)
    return optimized_path
```

## Rate Limits (Future)

Production API will implement rate limits:

- **Free tier**: 100 requests/day
- **Paid tier**: Custom limits

## Webhooks (Future)

Instead of polling, you can register webhooks:

```json
POST /webhooks/
{
  "url": "https://your-domain.com/webhook",
  "events": ["tryon.completed", "tryon.failed"]
}
```

## Support

For API support:
- Email: support@example.com
- GitHub Issues: https://github.com/eliasndungu/Virtual-Try-On-AI-for-Clothes-Shoes/issues
