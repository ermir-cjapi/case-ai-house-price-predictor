# Docker Setup Guide

## Overview

This project includes a complete Docker Compose setup that orchestrates all services needed for the House Price Predictor application with Celery task queue integration.

## Services

The `docker-compose.yml` defines 5 services:

1. **Redis** - Message broker and result backend
2. **Backend** - FastAPI application
3. **Celery Worker** - Background task processor
4. **Flower** - Celery monitoring UI
5. **Frontend** - Next.js web application

## Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine + Docker Compose (Linux)
- Minimum 4GB RAM allocated to Docker
- At least 10GB free disk space

### Install Docker

**Windows:**
1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. Run installer
3. Restart computer
4. Verify: `docker --version`

**Mac:**
1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
2. Drag to Applications
3. Open Docker Desktop
4. Verify: `docker --version`

**Linux (Ubuntu/Debian):**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker --version
docker compose version
```

## Quick Start

### Start All Services

**Windows:**
```bash
start-all.bat
```

**Linux/Mac:**
```bash
chmod +x start-all.sh
./start-all.sh
```

**Or directly:**
```bash
docker-compose up --build
```

### Start in Background (Detached Mode)

```bash
docker-compose up -d --build
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f celery-worker
docker-compose logs -f flower
docker-compose logs -f frontend
docker-compose logs -f redis
```

### Stop Services

```bash
# Stop (containers can be restarted)
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes (deletes Redis data and trained models)
docker-compose down -v
```

## Access Services

Once running, access the services at:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main web interface |
| **Backend API** | http://localhost:5000 | REST API |
| **API Docs** | http://localhost:5000/docs | Interactive Swagger UI |
| **Flower** | http://localhost:5555 | Celery monitoring dashboard |
| **Redis** | localhost:6379 | Direct Redis connection (for tools) |

## Development Workflow

### Build and Start

```bash
# Build images
docker-compose build

# Start services
docker-compose up

# Or combined
docker-compose up --build
```

### Hot Reloading

The Docker setup supports hot reloading:

**Backend:**
- Changes to Python files automatically reload FastAPI (via `--reload`)
- Volume mounted: `./backend:/app`

**Frontend:**
- Next.js development mode not enabled by default (production build)
- For development, run frontend locally instead

### Making Code Changes

1. **Backend changes:**
   - Edit files in `./backend`
   - FastAPI automatically reloads
   - No rebuild needed

2. **Celery task changes:**
   - Edit `backend/celery_tasks.py`
   - Restart worker: `docker-compose restart celery-worker`

3. **Frontend changes:**
   - Edit files in `./frontend`
   - Rebuild: `docker-compose up --build frontend`

4. **Dependency changes:**
   - Edit `requirements.txt` or `package.json`
   - Rebuild: `docker-compose build`

## Docker Commands Reference

### Container Management

```bash
# List running containers
docker-compose ps

# Restart a service
docker-compose restart backend

# Stop a service
docker-compose stop backend

# Start a stopped service
docker-compose start backend

# Remove a service container
docker-compose rm backend

# Scale workers (run multiple instances)
docker-compose up --scale celery-worker=3
```

### Execute Commands in Containers

```bash
# Open bash shell in backend
docker-compose exec backend bash

# Run Python script
docker-compose exec backend python train.py tensorflow

# Check Celery worker status
docker-compose exec celery-worker celery -A celery_app inspect active

# Check Redis
docker-compose exec redis redis-cli ping
```

### View Resource Usage

```bash
# CPU and memory usage
docker stats

# Disk usage
docker system df

# Detailed disk usage
docker system df -v
```

### Cleanup

```bash
# Remove stopped containers
docker-compose rm

# Remove unused images
docker image prune

# Remove all unused resources
docker system prune

# Remove everything (careful!)
docker system prune -a --volumes
```

## Volumes

The Docker setup uses named volumes for data persistence:

### `redis_data`
- Stores Redis database
- Persists task queue and results
- Survives container restarts

### `model_data`
- Stores trained ML models
- Shared between backend and celery-worker
- Survives container restarts

**View volumes:**
```bash
docker volume ls
```

**Inspect volume:**
```bash
docker volume inspect ai-deep-learning-example_model_data
```

**Backup volume:**
```bash
docker run --rm -v ai-deep-learning-example_model_data:/data -v $(pwd):/backup alpine tar czf /backup/models-backup.tar.gz -C /data .
```

**Restore volume:**
```bash
docker run --rm -v ai-deep-learning-example_model_data:/data -v $(pwd):/backup alpine tar xzf /backup/models-backup.tar.gz -C /data
```

## Environment Variables

### Backend (`backend` service)
```yaml
environment:
  - PORT=5000
  - REDIS_URL=redis://redis:6379/0
```

### Frontend (`frontend` service)
```yaml
environment:
  - BACKEND_URL=http://backend:5000
  - NODE_ENV=production
```

### Celery Worker (`celery-worker` service)
```yaml
environment:
  - REDIS_URL=redis://redis:6379/0
```

**Override with `.env` file:**

Create `.env` in project root:
```env
REDIS_URL=redis://redis:6379/0
PORT=5000
NODE_ENV=production
```

Docker Compose automatically loads this file.

## Networking

All services run on the `app-network` bridge network.

**Service DNS names:**
- `redis` - Redis server
- `backend` - FastAPI backend
- `celery-worker` - Celery worker
- `flower` - Flower monitoring
- `frontend` - Next.js frontend

Services can communicate using these names:
```python
# Backend connects to Redis
REDIS_URL = "redis://redis:6379/0"

# Frontend connects to Backend
BACKEND_URL = "http://backend:5000"
```

**Inspect network:**
```bash
docker network inspect ai-deep-learning-example_app-network
```

## Health Checks

### Redis Health Check
```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 10s
  timeout: 5s
  retries: 5
```

**Backend and workers wait for Redis to be healthy before starting.**

**Check health status:**
```bash
docker-compose ps
```

## Troubleshooting

### Port Already in Use

**Error:** `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Solution:**
```bash
# Find process using port
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :3000
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "3001:3000"  # Host:Container
```

### Container Fails to Start

**Check logs:**
```bash
docker-compose logs backend
```

**Common issues:**
1. **Dependency not installed:** Rebuild image
2. **Syntax error:** Fix code and restart
3. **Redis not ready:** Wait for health check

### Cannot Connect to Redis

**Verify Redis is running:**
```bash
docker-compose ps redis
```

**Test connection:**
```bash
docker-compose exec redis redis-cli ping
# Should return: PONG
```

**Check Redis logs:**
```bash
docker-compose logs redis
```

### Celery Worker Not Processing Tasks

**Check worker status:**
```bash
docker-compose logs celery-worker
```

**Verify worker is registered:**
```bash
docker-compose exec celery-worker celery -A celery_app inspect active
```

**Restart worker:**
```bash
docker-compose restart celery-worker
```

### Frontend Shows 502 Error

**Possible causes:**
1. Backend not ready
2. Wrong BACKEND_URL
3. Network issue

**Solutions:**
```bash
# Check backend is running
docker-compose ps backend

# Check backend logs
docker-compose logs backend

# Verify network connectivity
docker-compose exec frontend ping backend
```

### Models Not Persisting

**Issue:** Trained models disappear after restart

**Solution:** Ensure volume is mounted correctly
```yaml
volumes:
  - model_data:/app/backend/data
```

**Verify volume exists:**
```bash
docker volume ls | grep model_data
```

### Out of Memory

**Symptoms:**
- Containers keep restarting
- Training fails mysteriously
- Docker becomes unresponsive

**Solutions:**

1. **Increase Docker memory:**
   - Docker Desktop → Settings → Resources
   - Increase memory to 6-8GB

2. **Reduce concurrency:**
   ```yaml
   # In docker-compose.yml for celery-worker
   command: celery -A celery_app worker --loglevel=info --concurrency=1
   ```

3. **Reduce batch size or epochs:**
   - Train with fewer epochs
   - Smaller batch size in training code

### Slow Build Times

**Use BuildKit:**
```bash
# Windows (PowerShell)
$env:DOCKER_BUILDKIT=1
docker-compose build

# Linux/Mac
DOCKER_BUILDKIT=1 docker-compose build
```

**Use build cache:**
```bash
docker-compose build --parallel
```

**Clean up old images:**
```bash
docker image prune -a
```

## Production Deployment

### Security Best Practices

1. **Don't expose Redis directly:**
   ```yaml
   # Remove from redis service:
   # ports:
   #   - "6379:6379"
   ```

2. **Use secrets for sensitive data:**
   ```yaml
   secrets:
     redis_password:
       file: ./redis_password.txt
   ```

3. **Run as non-root user:**
   ```dockerfile
   USER nobody
   ```

4. **Use specific image tags:**
   ```yaml
   image: redis:7.2.3-alpine  # Not 'latest'
   ```

### Reverse Proxy (Nginx)

```nginx
# nginx.conf
upstream backend {
    server localhost:5000;
}

upstream frontend {
    server localhost:3000;
}

server {
    listen 80;
    server_name example.com;

    location /api {
        proxy_pass http://backend;
    }

    location / {
        proxy_pass http://frontend;
    }
}
```

### SSL/HTTPS

Use Let's Encrypt with Nginx:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

### Environment-Specific Configs

**docker-compose.prod.yml:**
```yaml
version: '3.8'

services:
  backend:
    environment:
      - NODE_ENV=production
      - DEBUG=False
    restart: always
  
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    restart: always
```

**Deploy:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Performance Optimization

### Multi-stage Builds

Already implemented in Dockerfiles to reduce image size.

### Layer Caching

Order Dockerfile commands from least to most frequently changed:
1. System dependencies
2. Application dependencies (requirements.txt)
3. Application code

### Parallel Builds

```bash
docker-compose build --parallel
```

### Resource Limits

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## Monitoring

### View Real-time Logs

```bash
# All services, color-coded
docker-compose logs -f --tail=100

# Filter by service
docker-compose logs -f backend celery-worker
```

### Monitor Resources

```bash
# Real-time resource usage
docker stats

# Container details
docker-compose ps
docker inspect <container_id>
```

### Flower Dashboard

Access at `http://localhost:5555` for:
- Task history
- Worker status
- Task execution times
- Success/failure rates

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Test

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build images
        run: docker-compose build
      
      - name: Start services
        run: docker-compose up -d
      
      - name: Wait for services
        run: sleep 30
      
      - name: Run tests
        run: docker-compose exec -T backend pytest
      
      - name: Stop services
        run: docker-compose down
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [FastAPI Docker Guide](https://fastapi.tiangolo.com/deployment/docker/)

---

**Enjoy containerized development! 🐳**

