#!/bin/bash

echo "========================================="
echo "Celery Integration Test Script"
echo "========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check service
check_service() {
    local url=$1
    local name=$2
    
    echo -n "Checking $name... "
    
    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "200\|301\|302"; then
        echo -e "${GREEN}✓ OK${NC}"
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        return 1
    fi
}

# Function to test with timeout
test_with_timeout() {
    local cmd=$1
    local timeout=5
    
    timeout $timeout bash -c "$cmd" 2>/dev/null
    return $?
}

echo "1. Checking if Docker is running..."
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}✗ Docker is not running!${NC}"
    echo "Please start Docker Desktop and try again."
    exit 1
fi
echo -e "${GREEN}✓ Docker is running${NC}"
echo ""

echo "2. Checking if services are up..."
if ! docker-compose ps | grep -q "Up"; then
    echo -e "${YELLOW}! Services are not running${NC}"
    echo "Starting services with docker-compose up -d..."
    docker-compose up -d
    echo "Waiting 30 seconds for services to start..."
    sleep 30
fi
echo ""

echo "3. Testing service endpoints..."

# Check Redis
echo -n "Checking Redis... "
if docker-compose exec -T redis redis-cli ping | grep -q "PONG"; then
    echo -e "${GREEN}✓ Redis is responding${NC}"
else
    echo -e "${RED}✗ Redis is not responding${NC}"
fi

# Check Backend
check_service "http://localhost:5000/health" "Backend API"

# Check Frontend
check_service "http://localhost:3000" "Frontend"

# Check Flower
check_service "http://localhost:5555" "Flower"

echo ""

echo "4. Testing Celery worker..."
echo -n "Checking worker status... "
if docker-compose exec -T celery-worker celery -A celery_app inspect active 2>&1 | grep -q "celery@"; then
    echo -e "${GREEN}✓ Worker is active${NC}"
else
    echo -e "${RED}✗ Worker is not responding${NC}"
fi
echo ""

echo "5. Testing Celery health endpoint..."
check_service "http://localhost:5000/celery/health" "Celery Health Check"
echo ""

echo "6. Submitting test training task..."
RESPONSE=$(curl -s -X POST "http://localhost:5000/train/tensorflow/async" \
  -H "Content-Type: application/json" \
  -d '{"epochs": 10}')

if echo "$RESPONSE" | grep -q "task_id"; then
    TASK_ID=$(echo "$RESPONSE" | grep -o '"task_id":"[^"]*"' | cut -d'"' -f4)
    echo -e "${GREEN}✓ Task submitted successfully${NC}"
    echo "Task ID: $TASK_ID"
    
    echo ""
    echo "7. Checking task status..."
    sleep 2
    
    STATUS_RESPONSE=$(curl -s "http://localhost:5000/task/$TASK_ID/status")
    STATE=$(echo "$STATUS_RESPONSE" | grep -o '"state":"[^"]*"' | cut -d'"' -f4)
    
    if [ ! -z "$STATE" ]; then
        echo -e "${GREEN}✓ Task status retrieved${NC}"
        echo "Current state: $STATE"
    else
        echo -e "${RED}✗ Failed to get task status${NC}"
    fi
else
    echo -e "${RED}✗ Failed to submit task${NC}"
    echo "Response: $RESPONSE"
fi

echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo ""
echo "Services running:"
docker-compose ps
echo ""
echo "Access points:"
echo "  - Frontend:  http://localhost:3000"
echo "  - API Docs:  http://localhost:5000/docs"
echo "  - Flower:    http://localhost:5555"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f [service]"
echo ""
echo "To stop services:"
echo "  docker-compose down"
echo ""
echo -e "${GREEN}Setup verification complete!${NC}"

