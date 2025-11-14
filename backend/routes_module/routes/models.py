"""
Model information and status endpoints
"""
from fastapi import APIRouter, HTTPException
import os
from schemas.model import ModelInfoResponse
from router.model_selector import get_model_characteristics
from routes_module.dependencies import models

router = APIRouter()


@router.get("/models/status", response_model=ModelInfoResponse)
async def models_status():
    """Get status and information about all models"""
    try:
        model_info = {}
        characteristics = get_model_characteristics()
        
        for model_type, model in models.items():
            # Check if model is trained
            model_file = f"backend/trained_models/model_{model_type}"
            model_file += ".keras" if model_type == "tensorflow" else ".pt"
            is_trained = os.path.exists(model_file)
            
            model_info[model_type] = {
                "trained": is_trained,
                "characteristics": characteristics.get(model_type, {}),
                "model_file": model_file
            }
        
        return ModelInfoResponse(
            success=True,
            models=model_info,
            message="Model status retrieved successfully"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting model status: {str(e)}"
        )


@router.get("/models/characteristics")
async def get_models_characteristics():
    """Get detailed characteristics of all model types"""
    return get_model_characteristics()

