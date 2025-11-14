"""
FastAPI application initialization and configuration
Main application file for the house price prediction API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from config import (
    API_TITLE, 
    API_DESCRIPTION, 
    API_VERSION, 
    API_HOST, 
    API_PORT,
    CORS_ORIGINS,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOW_METHODS,
    CORS_ALLOW_HEADERS
)
from routes_module.dependencies import models
from routes_module.routes import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup/shutdown"""
    # Startup: Load models if available
    for model_type, model in models.items():
        try:
            model.load_model()
            print(f"{model_type.upper()} model loaded successfully")
        except FileNotFoundError:
            print(f"No existing {model_type} model found. Train it first.")
    
    yield  # Application runs here
    
    # Shutdown: cleanup code here if needed


# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

# Include all API routes
app.include_router(api_router)


if __name__ == '__main__':
    import uvicorn
    
    print(f"\nStarting Multi-Model FastAPI server on port {API_PORT}...")
    print(f"API endpoints:")
    print(f"  - GET  /health              - Health check")
    print(f"  - GET  /celery/health       - Celery worker health check")
    print(f"  - GET  /models/status       - Model status")
    print(f"  - GET  /models/characteristics - Model details")
    print(f"  - POST /train/{{model_type}} - Train model (synchronous)")
    print(f"  - POST /train/{{model_type}}/async - Train model (async with Celery)")
    print(f"  - GET  /task/{{task_id}}/status - Get async task status")
    print(f"  - GET  /task/{{task_id}}/result - Get async task result")
    print(f"  - POST /predict             - Predict with routing")
    print(f"  - POST /predict/compare     - Compare all models")
    print(f"  - GET  /docs                - Interactive API docs")
    print()
    
    uvicorn.run(app, host=API_HOST, port=API_PORT)

