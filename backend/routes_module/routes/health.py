"""
Health check endpoints
"""
from fastapi import APIRouter
from schemas.health import HealthResponse
from celery_worker import health_check

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Multi-model API is running",
        available_models=["tensorflow", "pytorch", "xgboost", "ensemble"]
    )


@router.get("/celery/health")
async def celery_health():
    """Check if Celery worker is responsive"""
    try:
        # Submit a simple health check task with timeout
        result = health_check.apply_async()
        response = result.get(timeout=5)
        return {
            'success': True,
            'celery_status': 'connected',
            'worker_response': response
        }
    except Exception as e:
        return {
            'success': False,
            'celery_status': 'disconnected',
            'error': str(e)
        }

