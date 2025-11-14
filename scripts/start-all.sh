#!/bin/bash

echo "========================================"
echo "Starting House Price Predictor Stack"
echo "========================================"
echo ""
echo "This will start:"
echo "  - Redis (Message Broker)"
echo "  - Backend (FastAPI)"
echo "  - Celery Worker"
echo "  - Flower (Celery Monitor)"
echo "  - Frontend (Next.js)"
echo ""
echo "Services will be available at:"
echo "  - Frontend:       http://localhost:3000"
echo "  - Backend API:    http://localhost:5000"
echo "  - API Docs:       http://localhost:5000/docs"
echo "  - Flower UI:      http://localhost:5555"
echo ""
echo "Press Ctrl+C to stop all services"
echo "========================================"
echo ""

docker-compose up --build

