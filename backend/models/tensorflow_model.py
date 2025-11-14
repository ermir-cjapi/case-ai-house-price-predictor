"""
TensorFlow/Keras Neural Network implementation for house price prediction
Refactored to use base model interface
"""
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import Callback
import pickle
from typing import List
from .base_model import BaseHousingModel


class TrainingProgressCallback(Callback):
    """Callback to track training progress"""
    def __init__(self):
        super().__init__()
        self.losses = []
    
    def on_epoch_end(self, epoch, logs=None):
        self.losses.append(logs.get('loss'))
        if (epoch + 1) % 100 == 0:
            print(f"Epoch {epoch + 1}, Loss: {logs.get('loss'):.4f}")


class TensorFlowModel(BaseHousingModel):
    """
    Neural Network using TensorFlow/Keras for regression tasks
    Implements BaseHousingModel interface
    """
    
    def __init__(self, input_size=8, hidden_sizes=[64, 32, 16], output_size=1, learning_rate=0.001):
        """
        Initialize neural network using Keras Sequential API
        
        Args:
            input_size: Number of input features
            hidden_sizes: List of hidden layer sizes (e.g., [64, 32, 16])
            output_size: Number of output neurons (1 for regression)
            learning_rate: Learning rate for Adam optimizer
        """
        super().__init__(input_size, hidden_sizes, output_size, learning_rate)
        self.model = self._build_model()
    
    def _build_model(self):
        """Build the Keras model architecture"""
        model = models.Sequential()
        
        # Input layer
        model.add(layers.Input(shape=(self.input_size,)))
        
        # Hidden layers with ReLU activation
        for i, units in enumerate(self.hidden_sizes):
            model.add(layers.Dense(
                units,
                activation='relu',
                kernel_initializer='he_normal',  # He initialization for ReLU
                name=f'hidden_{i+1}'
            ))
        
        # Output layer (linear activation for regression)
        model.add(layers.Dense(
            self.output_size,
            activation='linear',
            name='output'
        ))
        
        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss='mse',  # Mean Squared Error
            metrics=['mae']  # Mean Absolute Error
        )
        
        return model
    
    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 500, 
              batch_size: int = 32, verbose: bool = True) -> List[float]:
        """
        Train the neural network
        
        Args:
            X: Training data
            y: Training labels
            epochs: Number of training epochs
            batch_size: Batch size for training
            verbose: Print training progress
        
        Returns:
            Training history with losses per epoch
        """
        # Create progress callback
        progress_callback = TrainingProgressCallback()
        
        # Train the model
        history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            verbose=0,  # We use custom callback for progress
            callbacks=[progress_callback] if verbose else []
        )
        
        # Store training history
        self.training_history = history.history
        
        return progress_callback.losses if verbose else history.history['loss']
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions on new data
        
        Args:
            X: Input data
        
        Returns:
            Predictions
        """
        return self.model.predict(X, verbose=0)
    
    def save(self, filepath: str) -> None:
        """Save model to file"""
        # Remove .pkl extension if present and add .keras
        if filepath.endswith('.pkl'):
            filepath = filepath[:-4]
        
        # Save model in Keras format
        self.model.save(f"{filepath}.keras")
        
        # Save metadata
        metadata = {
            'input_size': self.input_size,
            'hidden_sizes': self.hidden_sizes,
            'output_size': self.output_size,
            'learning_rate': self.learning_rate,
            'model_type': 'tensorflow'
        }
        with open(f"{filepath}_metadata.pkl", 'wb') as f:
            pickle.dump(metadata, f)
    
    def load(self, filepath: str) -> None:
        """Load model from file"""
        # Remove .pkl extension if present
        if filepath.endswith('.pkl'):
            filepath = filepath[:-4]
        
        # Load model
        self.model = keras.models.load_model(f"{filepath}.keras")
        
        # Load metadata
        with open(f"{filepath}_metadata.pkl", 'rb') as f:
            metadata = pickle.load(f)
            self.input_size = metadata['input_size']
            self.hidden_sizes = metadata['hidden_sizes']
            self.output_size = metadata['output_size']
            self.learning_rate = metadata['learning_rate']
    
    def summary(self) -> None:
        """Print model architecture summary"""
        return self.model.summary()
    
    def get_param_count(self) -> int:
        """Get total number of trainable parameters"""
        return self.model.count_params()

