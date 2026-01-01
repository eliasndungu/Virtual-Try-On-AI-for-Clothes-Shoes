# Virtual Try-On AI - Development Guide

## Development Setup

### Backend Development

1. **Create virtual environment:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run tests:**
```bash
pytest
```

4. **Run development server:**
```bash
python run.py
# Or with uvicorn directly:
uvicorn app.main:app --reload
```

5. **Access API documentation:**
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Frontend Development

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Run development server:**
```bash
npm run dev
```

3. **Build for production:**
```bash
npm run build
npm start
```

## Code Style

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints
- Document functions with docstrings
- Maximum line length: 100 characters

### TypeScript (Frontend)

- Follow ESLint configuration
- Use TypeScript for all new code
- Use functional components with hooks

## Testing

### Backend Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_image_processing.py

# Run with coverage
pytest --cov=app tests/

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

### Frontend Tests

```bash
# Run tests (when implemented)
npm test

# Run with coverage
npm run test:coverage
```

## Adding New Features

### 1. Add a New API Endpoint

1. Create endpoint in `backend/app/api/`:
```python
# backend/app/api/my_feature.py
from fastapi import APIRouter

router = APIRouter(prefix="/my-feature", tags=["My Feature"])

@router.get("/")
async def my_endpoint():
    return {"message": "Hello"}
```

2. Register router in `backend/app/api/__init__.py`:
```python
from .my_feature import router as my_feature_router

api_router.include_router(my_feature_router)
```

3. Add tests in `backend/tests/test_my_feature.py`

### 2. Add a New Database Model

1. Create model in `backend/app/models/database.py`:
```python
class MyModel(Base):
    __tablename__ = "my_table"
    id = Column(Integer, primary_key=True)
    name = Column(String)
```

2. Create Pydantic schema in `backend/app/models/schemas.py`:
```python
class MyModelSchema(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True
```

3. Create migration:
```bash
alembic revision --autogenerate -m "Add MyModel"
alembic upgrade head
```

### 3. Add a New Frontend Component

1. Create component in `frontend/src/components/`:
```tsx
// MyComponent.tsx
export default function MyComponent() {
    return <div>My Component</div>
}
```

2. Create styles in `frontend/src/components/MyComponent.module.css`

3. Import and use in pages

## Database Migrations

### Create a new migration

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migration

```bash
alembic downgrade -1
```

## Environment Variables

### Backend

Create `backend/.env` file:
```env
DATABASE_URL=sqlite+aiosqlite:///./virtual_tryon.db
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760
```

### Frontend

Create `frontend/.env.local` file:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Debugging

### Backend Debugging

1. **Add breakpoint:**
```python
import pdb; pdb.set_trace()
```

2. **Enable debug logs:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

3. **Use VS Code debugger:**
Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": ["app.main:app", "--reload"],
            "jinja": true,
            "cwd": "${workspaceFolder}/backend"
        }
    ]
}
```

### Frontend Debugging

Use browser DevTools or VS Code debugger.

## Common Tasks

### Add a new Python dependency

```bash
cd backend
pip install package-name
pip freeze > requirements.txt
```

### Add a new npm package

```bash
cd frontend
npm install package-name
```

### Clear database

```bash
cd backend
rm virtual_tryon.db
python -c "from app.services import db_service; import asyncio; asyncio.run(db_service.init_db())"
```

### Generate API client

```bash
# Generate TypeScript client from OpenAPI
curl http://localhost:8000/openapi.json > openapi.json
npx openapi-typescript openapi.json --output frontend/src/types/api.ts
```

## Troubleshooting

### Backend won't start

1. Check virtual environment is activated
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Check port 8000 is not in use: `lsof -i :8000`

### Frontend won't build

1. Clear Next.js cache: `rm -rf .next`
2. Reinstall dependencies: `rm -rf node_modules && npm install`
3. Check Node version: `node --version` (should be 18+)

### Tests failing

1. Check PYTHONPATH is set
2. Ensure test database is clean
3. Check for port conflicts

## Git Workflow

1. Create feature branch:
```bash
git checkout -b feature/my-feature
```

2. Make changes and commit:
```bash
git add .
git commit -m "Add my feature"
```

3. Push and create PR:
```bash
git push origin feature/my-feature
```

## Performance Tips

- Use async/await for I/O operations
- Implement caching for expensive operations
- Optimize database queries
- Lazy load frontend components
- Use CDN for static assets

## Security Considerations

- Never commit secrets to git
- Use environment variables for sensitive data
- Validate all user inputs
- Sanitize file uploads
- Use HTTPS in production
- Implement rate limiting
- Keep dependencies updated
