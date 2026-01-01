# Virtual Try-On AI System

An AI-powered virtual try-on system for clothes and shoes that allows retail shops to integrate via API or use a standalone dashboard.

## 🎯 Features

- **Upper-body clothing virtual try-on** (MVP scope)
- **Fixed poses support**: Front, Side, Three-Quarter
- **Visual preview** focused on appearance, not perfect fit
- **Image input** (photo upload)
- **API-first architecture** for easy integration
- **Dashboard interface** for standalone usage
- **Modular design** for extensibility

## 🏗️ Architecture

```
├── backend/           # FastAPI backend server
│   ├── app/
│   │   ├── api/       # API endpoints
│   │   ├── core/      # Core configuration
│   │   ├── models/    # Database and Pydantic models
│   │   ├── services/  # Business logic
│   │   └── utils/     # Utility functions
│   └── tests/         # Backend tests
├── frontend/          # Next.js dashboard
│   └── src/
│       ├── app/       # Next.js app pages
│       ├── components/# React components
│       └── services/  # API client
├── models/            # AI model weights (placeholder)
└── docs/              # Documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose (optional)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/eliasndungu/Virtual-Try-On-AI-for-Clothes-Shoes.git
cd Virtual-Try-On-AI-for-Clothes-Shoes

# Start all services
docker-compose up -d

# Access the services
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Frontend Dashboard: http://localhost:3000
```

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run the backend
python run.py

# Backend will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Frontend will be available at http://localhost:3000
```

## 📚 API Documentation

### Health Check

```bash
GET /api/v1/health
```

Response:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "supported_poses": ["front", "side", "three-quarter"]
}
```

### Create Try-On Request

```bash
POST /api/v1/tryon/
Content-Type: multipart/form-data

person_image: <file>
garment_image: <file>
pose: front|side|three-quarter (default: front)
```

Response:
```json
{
  "request_id": 1,
  "status": "pending",
  "message": "Try-on request created successfully",
  "created_at": "2024-01-01T00:00:00"
}
```

### Get Try-On Result

```bash
GET /api/v1/tryon/{request_id}
```

Response:
```json
{
  "id": 1,
  "status": "completed",
  "result_image_path": "uploads/results/result_xyz.jpg",
  "pose": "front",
  "processing_time": 2.5,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:03"
}
```

### API Key Management

```bash
# Create API Key
POST /api/v1/api-keys/
{
  "name": "My Integration"
}

# List API Keys
GET /api/v1/api-keys/

# Deactivate API Key
DELETE /api/v1/api-keys/{key_id}
```

## 🔌 Integration Guide

### REST API Integration

```python
import requests

# Create a try-on request
url = "http://localhost:8000/api/v1/tryon/"
files = {
    'person_image': open('person.jpg', 'rb'),
    'garment_image': open('garment.jpg', 'rb')
}
data = {'pose': 'front'}

response = requests.post(url, files=files, data=data)
result = response.json()
request_id = result['request_id']

# Poll for result
import time
while True:
    status_response = requests.get(f"{url}{request_id}")
    status = status_response.json()
    
    if status['status'] in ['completed', 'failed']:
        break
    
    time.sleep(2)

# Get result image
if status['status'] == 'completed':
    image_url = f"http://localhost:8000/{status['result_image_path']}"
    print(f"Result: {image_url}")
```

### JavaScript Integration

```javascript
const formData = new FormData();
formData.append('person_image', personImageFile);
formData.append('garment_image', garmentImageFile);
formData.append('pose', 'front');

const response = await fetch('http://localhost:8000/api/v1/tryon/', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log('Request ID:', result.request_id);

// Poll for result
const checkStatus = async (requestId) => {
  const statusResponse = await fetch(
    `http://localhost:8000/api/v1/tryon/${requestId}`
  );
  const status = await statusResponse.json();
  return status;
};
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Run Specific Test

```bash
pytest tests/test_image_processing.py -v
```

## 📦 Project Structure Details

### Backend Components

- **API Layer**: RESTful endpoints for try-on operations
- **Service Layer**: Business logic for image processing and AI inference
- **Model Layer**: Database models and Pydantic schemas
- **Utils**: Image processing, file handling utilities

### Frontend Components

- **TryOnUpload**: Component for uploading person and garment images
- **ResultDisplay**: Component for displaying try-on results
- **API Service**: Axios-based API client

## 🔧 Configuration

### Backend Environment Variables

See `backend/.env.example` for all configuration options.

Key settings:
- `DATABASE_URL`: Database connection string
- `UPLOAD_DIR`: Directory for uploaded images
- `MAX_UPLOAD_SIZE`: Maximum upload file size
- `SUPPORTED_POSES`: List of supported poses

### Frontend Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API URL

## 🛠️ Development

### Adding a New Pose

1. Add pose to `backend/app/core/config.py`:
```python
SUPPORTED_POSES: List[str] = ["front", "side", "three-quarter", "new_pose"]
```

2. Update `backend/app/models/schemas.py`:
```python
class PoseType(str, Enum):
    FRONT = "front"
    SIDE = "side"
    THREE_QUARTER = "three-quarter"
    NEW_POSE = "new_pose"
```

3. Update frontend pose selector in `frontend/src/components/TryOnUpload.tsx`

## 📝 MVP Scope & Limitations

**Current MVP includes:**
- ✅ Upper-body clothing virtual try-on
- ✅ Fixed poses (front, side, three-quarter)
- ✅ Visual preview generation
- ✅ Image input only
- ✅ RESTful API
- ✅ Web dashboard

**Not included in MVP:**
- ❌ Lower-body clothing (pants, skirts)
- ❌ Shoes virtual try-on
- ❌ Dynamic pose detection
- ❌ Perfect fit calculation
- ❌ Video input
- ❌ 3D rendering
- ❌ Production-ready AI model (placeholder implementation)

## 🚧 Roadmap

### Phase 1: MVP (Current)
- [x] Basic API structure
- [x] Image upload and processing
- [x] Dashboard UI
- [x] Placeholder try-on logic

### Phase 2: AI Model Integration
- [ ] Integrate HR-VITON or similar model
- [ ] Pose estimation
- [ ] Segmentation models
- [ ] Model optimization

### Phase 3: Enhanced Features
- [ ] Shoes try-on
- [ ] Lower-body clothing
- [ ] Multiple garments
- [ ] Size recommendations
- [ ] User accounts

### Phase 4: Production Ready
- [ ] Performance optimization
- [ ] CDN integration
- [ ] Analytics
- [ ] Payment integration
- [ ] Multi-tenancy

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙋 Support

For questions or issues, please open an issue on GitHub.

## 🔗 Related Technologies

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Next.js](https://nextjs.org/) - React framework
- [PyTorch](https://pytorch.org/) - Deep learning framework
- [HR-VITON](https://github.com/sangyun884/HR-VITON) - Virtual try-on research

## 🎓 AI Model Notes

The current implementation uses a **placeholder** for the virtual try-on AI model. For production use, you should integrate a real virtual try-on model such as:

- **HR-VITON**: High-Resolution Virtual Try-On Network
- **VITON-HD**: Virtual Try-On with High Definition
- **TryOnGAN**: Generative Adversarial Network for try-on
- **ClothFormer**: Transformer-based try-on model

Model integration points are clearly marked in `backend/app/services/tryon_service.py`.
