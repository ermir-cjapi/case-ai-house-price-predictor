"""
Shared dependencies and utilities for API routes
"""
from services.training_service import HousePriceModel
from router.langgraph_router import create_model_router
from schemas.predict import PredictRequest

# Global model instances
models = {
    'tensorflow': HousePriceModel(model_type='tensorflow'),
    'pytorch': HousePriceModel(model_type='pytorch'),
    'xgboost': HousePriceModel(model_type='xgboost')
}

# LangGraph router
router = create_model_router()


def build_features_dict(request: PredictRequest) -> dict:
    """Helper function to build features dictionary from prediction request"""
    sqft = float(request.sqft)
    bedrooms = float(request.bedrooms)
    bathrooms = float(request.bathrooms)
    latitude = float(request.latitude)
    longitude = float(request.longitude)
    median_income = float(request.median_income)
    house_age = float(request.house_age)
    population = float(request.population)
    
    # Calculate derived features
    ave_rooms = sqft / 200
    ave_bedrms = bedrooms
    ave_occup = population / 500 if population > 0 else 3.0
    
    return {
        'MedInc': median_income,
        'HouseAge': house_age,
        'AveRooms': ave_rooms,
        'AveBedrms': ave_bedrms,
        'Population': population,
        'AveOccup': ave_occup,
        'Latitude': latitude,
        'Longitude': longitude
    }

