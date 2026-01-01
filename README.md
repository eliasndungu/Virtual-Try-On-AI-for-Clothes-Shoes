# Virtual Try-On AI for Clothes & Shoes

An AI-powered virtual try-on system that enables fashion retail shops to offer customers a visual preview of how clothes and shoes look on them before physical fitting.

## 🎯 Overview

A modular, API-first system where retail shops can either:
- **Integrate via API** into their POS/e-commerce system
- **Use a standalone dashboard** for direct customer interaction

**How it works:** Customers upload a photo → AI visualizes how outfits and shoes would look on their body

## 🚀 MVP Features

- ✅ **Upper-body clothing** virtual try-on
- ✅ **Fixed poses** support (front, side, three-quarter)
- ✅ **Visual preview** focused on appearance
- ✅ **Image input only** (no video)
- ✅ **RESTful API** for easy integration
- ✅ **Web dashboard** for standalone usage

## 📋 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/eliasndungu/Virtual-Try-On-AI-for-Clothes-Shoes.git
cd Virtual-Try-On-AI-for-Clothes-Shoes

# Start all services
docker-compose up -d

# Access the services
# Backend API: http://localhost:8000/docs
# Frontend Dashboard: http://localhost:3000
```

### Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📚 Documentation

For detailed documentation, see [docs/README.md](docs/README.md)

- **API Documentation**: Available at http://localhost:8000/docs
- **Integration Guide**: See docs/README.md
- **Architecture**: See project structure in docs

## 🏗️ Technology Stack

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy (Database ORM)
- Pillow & OpenCV (Image processing)
- PyTorch (Deep learning - placeholder)

**Frontend:**
- Next.js 14 (React framework)
- TypeScript
- CSS Modules

**Infrastructure:**
- Docker & Docker Compose
- SQLite (Development database)

## 🔌 API Example

```python
import requests

# Create try-on request
files = {
    'person_image': open('person.jpg', 'rb'),
    'garment_image': open('shirt.jpg', 'rb')
}
response = requests.post('http://localhost:8000/api/v1/tryon/', files=files)
print(response.json())
```

## 📦 Project Structure

```
├── backend/           # FastAPI backend
│   ├── app/           # Application code
│   │   ├── api/       # API endpoints
│   │   ├── models/    # Data models
│   │   ├── services/  # Business logic
│   │   └── utils/     # Utilities
│   └── tests/         # Tests
├── frontend/          # Next.js dashboard
│   └── src/
│       ├── app/       # Pages
│       └── components/# UI components
├── models/            # AI model weights
└── docs/              # Documentation
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend (when implemented)
cd frontend
npm test
```

## 🛠️ Development Status

**Current Phase: MVP** ✅

- [x] Project structure
- [x] Backend API
- [x] Frontend dashboard
- [x] Image processing
- [x] Database models
- [x] Docker setup
- [x] Documentation

**Next Phase: AI Model Integration**

- [ ] Integrate HR-VITON or similar model
- [ ] Pose estimation
- [ ] Garment segmentation
- [ ] Model optimization

## 📝 MVP Scope & Limitations

**Included:**
- Upper-body clothing try-on
- Fixed poses (3 types)
- Visual preview generation
- RESTful API & Dashboard

**Not Included (Future):**
- Lower-body clothing & shoes
- Dynamic pose detection
- Perfect fit calculation
- Video input
- Production AI model (using placeholder)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙋 Support

For questions or issues, please [open an issue](https://github.com/eliasndungu/Virtual-Try-On-AI-for-Clothes-Shoes/issues) on GitHub.

## 🔗 Links

- [API Documentation](http://localhost:8000/docs) (when running)
- [Detailed Documentation](docs/README.md)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)
