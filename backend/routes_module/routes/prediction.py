"""
Prediction endpoints
"""
from fastapi import APIRouter, HTTPException
import numpy as np
from schemas.predict import PredictRequest, PredictResponse, CompareResponse
from routes_module.dependencies import models, router as langgraph_router, build_features_dict

router = APIRouter()


@router.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """
    Predict house price using LangGraph routing
    
    The model is automatically selected based on preference and criteria,
    or you can specify a model explicitly.
    """
    try:
        # Build features dictionary
        features = build_features_dict(request)
        
        # Use LangGraph router to select model
        routing_result = langgraph_router.route(
            features=features,
            model_preference=request.model_preference,
            criteria=request.criteria
        )
        
        selected_model = routing_result['selected_model']
        
        # Handle ensemble
        if selected_model == 'ensemble':
            predictions = {}
            for model_type, model in models.items():
                try:
                    pred = model.predict(features)
                    predictions[model_type] = pred
                except Exception as e:
                    print(f"Error with {model_type}: {e}")
            
            if not predictions:
                raise HTTPException(
                    status_code=404,
                    detail="No trained models available for ensemble"
                )
            
            # Average predictions
            avg_prediction = np.mean(list(predictions.values()))
            price_dollars = avg_prediction * 100000
            
            return PredictResponse(
                success=True,
                predicted_price=round(price_dollars, 2),
                predicted_price_formatted=f"${price_dollars:,.2f}",
                model_used="ensemble",
                routing_explanation=routing_result['explanation'],
                features_used=features,
                ensemble_predictions={k: v * 100000 for k, v in predictions.items()}
            )
        else:
            # Single model prediction
            model = models[selected_model]
            predicted_price = model.predict(features)
            price_dollars = predicted_price * 100000
            
            return PredictResponse(
                success=True,
                predicted_price=round(price_dollars, 2),
                predicted_price_formatted=f"${price_dollars:,.2f}",
                model_used=selected_model,
                routing_explanation=routing_result['explanation'],
                features_used=features
            )
    
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Model not found. Please train the model first."
        )
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post("/predict/compare", response_model=CompareResponse)
async def predict_compare(request: PredictRequest):
    """
    Get predictions from all available models for comparison
    """
    try:
        features = build_features_dict(request)
        
        predictions = {}
        predictions_formatted = {}
        
        for model_type, model in models.items():
            try:
                pred = model.predict(features)
                price_dollars = pred * 100000
                predictions[model_type] = round(price_dollars, 2)
                predictions_formatted[model_type] = f"${price_dollars:,.2f}"
            except FileNotFoundError:
                predictions[model_type] = None
                predictions_formatted[model_type] = "Not trained"
        
        # Calculate average of available predictions
        available_preds = [p for p in predictions.values() if p is not None]
        avg_prediction = np.mean(available_preds) if available_preds else 0
        
        return CompareResponse(
            success=True,
            predictions=predictions,
            predictions_formatted=predictions_formatted,
            average_prediction=round(avg_prediction, 2),
            features_used=features
        )
    
    except Exception as e:
        print(f"Comparison error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Comparison failed: {str(e)}"
        )

