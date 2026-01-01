# Contributing to Virtual Try-On AI

Thank you for your interest in contributing to the Virtual Try-On AI project! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots if applicable

### Suggesting Features

We welcome feature suggestions! Please create an issue with:
- Clear description of the feature
- Use case and benefits
- Potential implementation approach (optional)

### Submitting Code

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style guidelines
   - Add tests for new functionality
   - Update documentation

4. **Commit your changes**
   ```bash
   git commit -m "Add: description of your changes"
   ```
   
   Use conventional commits:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation
   - `test:` for tests
   - `refactor:` for refactoring
   - `style:` for formatting

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Describe your changes
   - Reference any related issues
   - Ensure all tests pass

## 📋 Code Style Guidelines

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for functions and classes

Example:
```python
def process_image(image_path: str, size: Tuple[int, int]) -> Image.Image:
    """
    Process and resize an image.
    
    Args:
        image_path: Path to the image file
        size: Target size as (width, height)
        
    Returns:
        Processed PIL Image object
    """
    # Implementation
```

### TypeScript (Frontend)

- Follow ESLint configuration
- Use TypeScript for all new code
- Use functional components with hooks
- Use CSS Modules for styling

Example:
```typescript
interface UploadProps {
    onUpload: (file: File) => void;
}

export default function Upload({ onUpload }: UploadProps) {
    // Implementation
}
```

## 🧪 Testing

### Backend Tests

All new code must include tests:

```python
# tests/test_my_feature.py
import pytest
from app.services.my_feature import MyFeature

class TestMyFeature:
    def test_basic_functionality(self):
        feature = MyFeature()
        result = feature.process()
        assert result is not None
```

Run tests:
```bash
cd backend
pytest
```

### Frontend Tests

When implementing frontend tests:
```bash
cd frontend
npm test
```

## 📚 Documentation

- Update README.md for major changes
- Update API documentation for new endpoints
- Add docstrings to all functions
- Include usage examples

## 🔍 Code Review Process

1. **Automated Checks**
   - Tests must pass
   - Code must follow style guidelines
   - No security vulnerabilities

2. **Manual Review**
   - Code quality
   - Documentation completeness
   - Test coverage
   - Performance considerations

3. **Approval**
   - At least one maintainer approval required
   - All comments addressed

## 🎯 Priority Areas

We especially welcome contributions in:

1. **AI Model Integration**
   - Integrating production-ready virtual try-on models
   - Pose estimation improvements
   - Garment segmentation

2. **Performance**
   - Image processing optimization
   - API response time improvements
   - Database query optimization

3. **Features**
   - Shoes virtual try-on
   - Lower-body clothing support
   - Multi-garment try-on
   - Size recommendations

4. **Documentation**
   - Tutorial videos
   - Integration examples
   - Best practices guides

5. **Testing**
   - Integration tests
   - End-to-end tests
   - Performance tests

## 🚀 Development Setup

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed setup instructions.

Quick start:
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest

# Frontend
cd frontend
npm install
npm run dev
```

## 📝 Commit Message Guidelines

Use clear, descriptive commit messages:

Good:
```
feat: Add support for three-quarter pose
fix: Resolve image upload timeout issue
docs: Update API integration guide
```

Bad:
```
Update code
Fix bug
Changes
```

## 🏷️ Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `priority:high`: High priority
- `priority:low`: Low priority

## 💬 Communication

- **GitHub Issues**: For bug reports and feature requests
- **Pull Requests**: For code contributions
- **Discussions**: For questions and general discussion

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## ❓ Questions?

If you have questions about contributing:
1. Check existing issues and documentation
2. Create a new issue with the `question` label
3. Reach out to maintainers

Thank you for contributing to Virtual Try-On AI! 🎉
