"""
Services module for business logic
"""
from .training_service import HousePriceModel, train_all_models

__all__ = ['HousePriceModel', 'train_all_models']

