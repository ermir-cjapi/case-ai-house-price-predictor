@echo off
echo =========================================
echo Celery Integration Test Script
echo =========================================
echo.

echo 1. Checking if Docker is running...
docker info >nul 2>&1
if errorlevel 1 (
    echo [FAILED] Docker is not running!
    echo Please start Docker Desktop and try again.
    exit /b 1
)
echo [OK] Docker is running
echo.

echo 2. Checking if services are up...
docker-compose ps | findstr "Up" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Services are not running
    echo Starting services with docker-compose up -d...
    docker-compose up -d
    echo Waiting 30 seconds for services to start...
    timeout /t 30 /nobreak >nul
)
echo.

echo 3. Testing service endpoints...

echo Checking Redis...
docker-compose exec -T redis redis-cli ping | findstr "PONG" >nul 2>&1
if errorlevel 1 (
    echo [FAILED] Redis is not responding
) else (
    echo [OK] Redis is responding
)

echo Checking Backend API...
curl -s http://localhost:5000/health >nul 2>&1
if errorlevel 1 (
    echo [FAILED] Backend API is not responding
) else (
    echo [OK] Backend API is responding
)

echo Checking Frontend...
curl -s http://localhost:3000 >nul 2>&1
if errorlevel 1 (
    echo [FAILED] Frontend is not responding
) else (
    echo [OK] Frontend is responding
)

echo Checking Flower...
curl -s http://localhost:5555 >nul 2>&1
if errorlevel 1 (
    echo [FAILED] Flower is not responding
) else (
    echo [OK] Flower is responding
)

echo.

echo 4. Testing Celery worker...
echo Checking worker status...
docker-compose exec -T celery-worker celery -A celery_app inspect active 2>nul | findstr "celery@" >nul 2>&1
if errorlevel 1 (
    echo [FAILED] Worker is not responding
) else (
    echo [OK] Worker is active
)
echo.

echo 5. Testing Celery health endpoint...
curl -s http://localhost:5000/celery/health >nul 2>&1
if errorlevel 1 (
    echo [FAILED] Celery health endpoint not responding
) else (
    echo [OK] Celery health endpoint responding
)
echo.

echo 6. Submitting test training task...
curl -s -X POST "http://localhost:5000/train/tensorflow/async" -H "Content-Type: application/json" -d "{\"epochs\": 10}" > temp_response.json 2>&1
findstr "task_id" temp_response.json >nul 2>&1
if errorlevel 1 (
    echo [FAILED] Failed to submit task
    type temp_response.json
) else (
    echo [OK] Task submitted successfully
    type temp_response.json
)
del temp_response.json >nul 2>&1
echo.

echo =========================================
echo Test Summary
echo =========================================
echo.
echo Services running:
docker-compose ps
echo.
echo Access points:
echo   - Frontend:  http://localhost:3000
echo   - API Docs:  http://localhost:5000/docs
echo   - Flower:    http://localhost:5555
echo.
echo To view logs:
echo   docker-compose logs -f [service]
echo.
echo To stop services:
echo   docker-compose down
echo.
echo Setup verification complete!
pause

