"""
API routes initialization
Imports and combines all route modules
"""
from fastapi import APIRouter
from .health import router as health_router
from .training import router as training_router
from .prediction import router as prediction_router
from .models import router as models_router
from .tasks import router as tasks_router

# Create main API router
api_router = APIRouter()

# Include all route modules
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(training_router, tags=["Training"])
api_router.include_router(prediction_router, tags=["Prediction"])
api_router.include_router(models_router, tags=["Models"])
api_router.include_router(tasks_router, tags=["Tasks"])

__all__ = ['api_router']

