"""
Model training endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import Literal
from schemas.train import TrainRequest, TrainResponse, AsyncTrainResponse
from routes_module.dependencies import models
from celery_worker import train_model_async

router = APIRouter()


@router.post("/train/{model_type}", response_model=TrainResponse)
async def train(model_type: Literal['tensorflow', 'pytorch', 'huggingface', 'all'], 
                request: TrainRequest):
    """
    Train a specific model or all models
    
    Path parameter:
        model_type: tensorflow, pytorch, huggingface, or all
    
    Request body:
        - epochs: number of training epochs (default: 500)
        - learning_rate: learning rate for training (default: 0.001)
        - hidden_sizes: list of hidden layer sizes (default: [64, 32, 16])
    """
    try:
        if model_type == 'all':
            # Train all models
            results = {}
            for mt in ['tensorflow', 'pytorch', 'huggingface']:
                print(f"Training {mt} model...")
                model = models[mt]
                metrics = model.train_model(
                    epochs=request.epochs,
                    learning_rate=request.learning_rate,
                    hidden_sizes=request.hidden_sizes
                )
                results[mt] = metrics
            
            return TrainResponse(
                success=True,
                message="All models trained successfully",
                model_type="all",
                metrics=results
            )
        else:
            # Train specific model
            model = models[model_type]
            metrics = model.train_model(
                epochs=request.epochs,
                learning_rate=request.learning_rate,
                hidden_sizes=request.hidden_sizes
            )
            
            return TrainResponse(
                success=True,
                message=f"{model_type.upper()} model trained successfully",
                model_type=model_type,
                metrics=metrics
            )
    
    except Exception as e:
        print(f"Training error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Training failed: {str(e)}"
        )


@router.post("/train/{model_type}/async", response_model=AsyncTrainResponse)
async def train_async(model_type: Literal['tensorflow', 'pytorch', 'huggingface', 'all'], 
                      request: TrainRequest):
    """
    Submit asynchronous training task for a specific model or all models
    
    Returns immediately with a task_id that can be used to check status
    
    Path parameter:
        model_type: tensorflow, pytorch, huggingface, or all
    
    Request body:
        - epochs: number of training epochs (default: 500)
        - learning_rate: learning rate for training (default: 0.001)
        - hidden_sizes: list of hidden layer sizes (default: [64, 32, 16])
    """
    try:
        # Submit task to Celery
        task = train_model_async.apply_async(
            args=[model_type, request.epochs, request.learning_rate, request.hidden_sizes]
        )
        
        return AsyncTrainResponse(
            success=True,
            task_id=task.id,
            message=f"Training task submitted for {model_type}",
            model_type=model_type
        )
    
    except Exception as e:
        print(f"Error submitting training task: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to submit training task: {str(e)}"
        )

