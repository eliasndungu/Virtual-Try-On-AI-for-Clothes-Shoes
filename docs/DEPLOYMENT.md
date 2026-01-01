# Deployment Guide

## Production Deployment

This guide covers deploying the Virtual Try-On AI system to production.

## Prerequisites

- Docker & Docker Compose
- Domain name (optional)
- SSL certificate (for HTTPS)
- Cloud provider account (AWS, GCP, Azure, etc.)

## Docker Deployment

### 1. Build Images

```bash
# Build all services
docker-compose build

# Or build individually
docker build -t virtual-tryon-backend ./backend
docker build -t virtual-tryon-frontend ./frontend
```

### 2. Production Configuration

Create a `.env` file in the root directory:

```bash
# Backend
DATABASE_URL=postgresql://user:password@db:5432/virtual_tryon
UPLOAD_DIR=/app/uploads
MAX_UPLOAD_SIZE=10485760
BACKEND_CORS_ORIGINS=https://your-domain.com

# Frontend
NEXT_PUBLIC_API_URL=https://api.your-domain.com/api/v1
```

### 3. Deploy with Docker Compose

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 4. Set Up Reverse Proxy (Nginx)

```nginx
# /etc/nginx/sites-available/virtual-tryon

# Backend API
server {
    listen 80;
    server_name api.your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeout for long-running try-on requests
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Serve uploaded images
    location /uploads/ {
        alias /path/to/uploads/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}

# Frontend Dashboard
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/virtual-tryon /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. SSL with Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d api.your-domain.com
```

## Cloud Platform Deployment

### AWS Deployment

#### Option 1: EC2 with Docker

1. Launch EC2 instance (t3.medium or larger)
2. Install Docker and Docker Compose
3. Clone repository
4. Run docker-compose
5. Configure security groups (ports 80, 443)
6. Set up Application Load Balancer

#### Option 2: ECS with Fargate

```bash
# Build and push to ECR
aws ecr create-repository --repository-name virtual-tryon-backend
aws ecr create-repository --repository-name virtual-tryon-frontend

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t virtual-tryon-backend ./backend
docker tag virtual-tryon-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/virtual-tryon-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/virtual-tryon-backend:latest

# Create ECS task definition and service
aws ecs create-task-definition --cli-input-json file://ecs-task-def.json
aws ecs create-service --cluster virtual-tryon --service-name backend --task-definition virtual-tryon-backend
```

### Google Cloud Platform

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/virtual-tryon-backend ./backend
gcloud builds submit --tag gcr.io/PROJECT_ID/virtual-tryon-frontend ./frontend

# Deploy to Cloud Run
gcloud run deploy backend \
  --image gcr.io/PROJECT_ID/virtual-tryon-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

gcloud run deploy frontend \
  --image gcr.io/PROJECT_ID/virtual-tryon-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure

```bash
# Create container registry
az acr create --resource-group myResourceGroup --name virtualtryon --sku Basic

# Build and push
az acr build --registry virtualtryon --image backend:latest ./backend
az acr build --registry virtualtryon --image frontend:latest ./frontend

# Deploy to App Service
az webapp create --resource-group myResourceGroup --plan myPlan --name virtual-tryon-backend --deployment-container-image-name virtualtryon.azurecr.io/backend:latest
```

## Database Migration

### Development to Production

1. **Backup development data**
```bash
sqlite3 virtual_tryon.db .dump > backup.sql
```

2. **Switch to PostgreSQL for production**

Update `backend/.env`:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/virtual_tryon
```

3. **Run migrations**
```bash
cd backend
alembic upgrade head
```

## Monitoring & Logging

### 1. Application Logs

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Save logs to file
docker-compose logs > logs/app.log
```

### 2. Health Monitoring

Set up health check endpoints:

```bash
# Backend health
curl http://localhost:8000/api/v1/health

# Set up monitoring with cron
*/5 * * * * curl -f http://localhost:8000/api/v1/health || echo "Backend down" | mail -s "Alert" admin@example.com
```

### 3. Error Tracking

Integrate Sentry for error tracking:

```python
# backend/app/main.py
import sentry_sdk

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    traces_sample_rate=1.0,
)
```

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.prod.yml
services:
  backend:
    deploy:
      replicas: 3
    
  frontend:
    deploy:
      replicas: 2
```

### Load Balancing

Use Nginx as load balancer:

```nginx
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

## Backup Strategy

### 1. Database Backups

```bash
# Automated daily backups
0 2 * * * pg_dump virtual_tryon > /backups/db-$(date +\%Y\%m\%d).sql
```

### 2. Upload Directory Backups

```bash
# Sync to S3
aws s3 sync /app/uploads s3://your-bucket/uploads --delete
```

## Security Checklist

- [ ] Use HTTPS (SSL/TLS)
- [ ] Set up firewall rules
- [ ] Enable API rate limiting
- [ ] Implement API key authentication
- [ ] Regular security updates
- [ ] Use environment variables for secrets
- [ ] Enable CORS properly
- [ ] Sanitize user inputs
- [ ] Regular backups
- [ ] Monitor for suspicious activity

## Performance Optimization

### 1. Image Optimization

- Use CDN for serving images
- Implement image caching
- Compress uploaded images

### 2. API Optimization

- Add Redis for caching
- Implement request queuing
- Use async processing

### 3. Frontend Optimization

- Enable Next.js production mode
- Use CDN for static assets
- Implement lazy loading

## Maintenance

### Regular Updates

```bash
# Update dependencies
cd backend && pip install -U -r requirements.txt
cd frontend && npm update

# Rebuild and redeploy
docker-compose build
docker-compose up -d
```

### Database Maintenance

```bash
# Vacuum PostgreSQL
psql -U user -d virtual_tryon -c "VACUUM ANALYZE;"

# Clean old uploads (older than 30 days)
find /app/uploads -mtime +30 -delete
```

## Troubleshooting

### Backend Issues

```bash
# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend

# Check database connection
docker-compose exec backend python -c "from app.services import db_service; import asyncio; asyncio.run(db_service.init_db())"
```

### Frontend Issues

```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend
```

## Cost Optimization

- Use spot instances for non-critical workloads
- Implement auto-scaling
- Use object storage for uploads
- Monitor and optimize database queries
- Use serverless for infrequent tasks

## Support

For deployment support, please contact:
- GitHub Issues: https://github.com/eliasndungu/Virtual-Try-On-AI-for-Clothes-Shoes/issues
- Email: support@example.com
