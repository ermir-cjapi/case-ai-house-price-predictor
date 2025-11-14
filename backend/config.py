"""
Configuration settings for the house price prediction API
Centralizes all configuration variables and environment settings
"""
import os
from typing import List, Literal

# Model configuration
ModelType = Literal['tensorflow', 'pytorch', 'xgboost']
AVAILABLE_MODEL_TYPES: List[str] = ['tensorflow', 'pytorch', 'xgboost']

# Server configuration
API_PORT = int(os.environ.get('PORT', 5000))
API_HOST = "0.0.0.0"

# CORS configuration
CORS_ORIGINS = ["*"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# Redis/Celery configuration
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

# File paths
TRAINED_MODELS_DIR = 'backend/trained_models'
MODEL_PATH_TEMPLATE = f'{TRAINED_MODELS_DIR}/model_{{model_type}}'
SCALER_PATH_TEMPLATE = f'{TRAINED_MODELS_DIR}/scalers_{{model_type}}.pkl'

# Model training defaults
DEFAULT_EPOCHS = 500
DEFAULT_LEARNING_RATE = 0.001
DEFAULT_HIDDEN_SIZES = [64, 32, 16]

# Celery configuration
CELERY_CONFIG = {
    'task_serializer': 'json',
    'accept_content': ['json'],
    'result_serializer': 'json',
    'timezone': 'UTC',
    'enable_utc': True,
    'task_track_started': True,
    'task_time_limit': 3600,  # 1 hour max
    'task_soft_time_limit': 3300,  # 55 minutes soft limit
    'worker_prefetch_multiplier': 1,
    'worker_max_tasks_per_child': 10,
    'result_expires': 3600,  # Results expire after 1 hour
    'result_extended': True,  # Store more task metadata
}

# API metadata
API_TITLE = "Multi-Model House Price Predictor API"
API_DESCRIPTION = "API for training and predicting house prices using TensorFlow, PyTorch, and Transformer models with LangGraph routing"
API_VERSION = "2.0.0"

