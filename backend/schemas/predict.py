"""Prediction-related schemas"""
from pydantic import BaseModel, Field
from typing import Optional, Dict


class PredictRequest(BaseModel):
    sqft: float = Field(..., description="Square footage of the house")
    bedrooms: float = Field(..., description="Number of bedrooms")
    bathrooms: float = Field(..., description="Number of bathrooms")
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    median_income: Optional[float] = Field(default=3.5, description="Median income in area")
    house_age: Optional[float] = Field(default=25, description="Age of house in years")
    population: Optional[float] = Field(default=1500, description="Population in area")
    model_preference: Optional[str] = Field(default="auto", description="Model to use: auto, tensorflow, pytorch, huggingface, ensemble")
    criteria: Optional[Dict] = Field(default=None, description="Criteria for auto model selection")


class PredictResponse(BaseModel):
    success: bool
    predicted_price: Optional[float] = None
    predicted_price_formatted: Optional[str] = None
    model_used: Optional[str] = None
    routing_explanation: Optional[str] = None
    features_used: Optional[dict] = None
    ensemble_predictions: Optional[Dict[str, float]] = None
    message: Optional[str] = None


class CompareResponse(BaseModel):
    success: bool
    predictions: Dict[str, float]
    predictions_formatted: Dict[str, str]
    average_prediction: float
    features_used: dict

