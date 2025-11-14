"""
Neural Network Models for House Price Prediction

This package contains three implementations:
- TensorFlow/Keras model
- PyTorch model  
- Hugging Face Transformer model
"""
from .base_model import BaseHousingModel, calculate_r2_score

__all__ = ['BaseHousingModel', 'calculate_r2_score']

