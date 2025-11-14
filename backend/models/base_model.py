"""
Abstract base class for house price prediction models
Ensures consistent interface across TensorFlow, PyTorch, and Hugging Face implementations
"""
from abc import ABC, abstractmethod
from typing import Dict, List
import numpy as np


class BaseHousingModel(ABC):
    """
    Abstract base class for housing price prediction models
    
    All model implementations (TensorFlow, PyTorch, Hugging Face) must inherit from this
    and implement the required methods to ensure consistent interface.
    """
    
    def __init__(self, input_size: int, hidden_sizes: List[int], output_size: int, 
                 learning_rate: float = 0.001):
        """
        Initialize the model
        
        Args:
            input_size: Number of input features
            hidden_sizes: List of hidden layer sizes
            output_size: Number of output neurons
            learning_rate: Learning rate for optimizer
        """
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size
        self.learning_rate = learning_rate
        self.training_history = {}
        self.metrics = {}
    
    @abstractmethod
    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 500, 
              batch_size: int = 32, verbose: bool = True) -> List[float]:
        """
        Train the model
        
        Args:
            X: Training features
            y: Training labels
            epochs: Number of training epochs
            batch_size: Batch size for training
            verbose: Whether to print progress
            
        Returns:
            List of losses per epoch
        """
        pass
    
    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions
        
        Args:
            X: Input features
            
        Returns:
            Predictions
        """
        pass
    
    @abstractmethod
    def save(self, filepath: str) -> None:
        """
        Save model to disk
        
        Args:
            filepath: Path to save the model
        """
        pass
    
    @abstractmethod
    def load(self, filepath: str) -> None:
        """
        Load model from disk
        
        Args:
            filepath: Path to load the model from
        """
        pass
    
    @abstractmethod
    def summary(self) -> None:
        """
        Print model architecture summary
        """
        pass
    
    def get_metrics(self) -> Dict:
        """
        Get model metrics
        
        Returns:
            Dictionary of metrics (R², RMSE, etc.)
        """
        return self.metrics
    
    def get_architecture_info(self) -> Dict:
        """
        Get architecture information
        
        Returns:
            Dictionary with architecture details
        """
        return {
            'input_size': self.input_size,
            'hidden_sizes': self.hidden_sizes,
            'output_size': self.output_size,
            'learning_rate': self.learning_rate,
            'model_type': self.__class__.__name__
        }


def calculate_r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate R² (coefficient of determination) score
    
    Args:
        y_true: True values
        y_pred: Predicted values
        
    Returns:
        R² score (1.0 is perfect, 0.0 is baseline, negative is worse than baseline)
    """
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot)

