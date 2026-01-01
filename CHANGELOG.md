# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-01

### Added
- Initial MVP release
- Backend API with FastAPI
  - Virtual try-on endpoints
  - Image upload and processing
  - Database models for requests and API keys
  - Health check endpoint
- Frontend dashboard with Next.js
  - Image upload component
  - Pose selector (front, side, three-quarter)
  - Result display component
  - Polling for request status
- Image processing utilities
  - Image validation
  - Image resizing
  - Format conversion
- Placeholder virtual try-on service
  - Support for 3 fixed poses
  - Basic image composition for demo
- Docker configuration
  - Backend Dockerfile
  - Frontend Dockerfile
  - Docker Compose setup
- Documentation
  - README with quick start guide
  - API integration guide
  - Deployment guide
  - Architecture documentation
- Testing infrastructure
  - Unit tests for image processing
  - Unit tests for try-on service
  - Test fixtures and utilities

### Scope
- Upper-body clothing only
- Image input only (no video)
- Visual preview focus (not perfect fit)
- Fixed poses (3 types)

### Known Limitations
- Placeholder AI model (not production-ready)
- SQLite database (development only)
- No authentication/authorization
- No rate limiting
- No webhook support
