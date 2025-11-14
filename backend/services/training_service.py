"""
Training script for house price prediction
Supports TensorFlow, PyTorch, and Hugging Face Transformer models
"""
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
import os
from typing import Literal, Optional
from models.tensorflow_model import TensorFlowModel
from models.pytorch_model import PyTorchModel
from models.huggingface_model import HuggingFaceModel
from models.base_model import calculate_r2_score

ModelType = Literal['tensorflow', 'pytorch', 'huggingface']


class HousePriceModel:
    """Wrapper class for house price prediction supporting multiple model types"""
    
    def __init__(self, model_type: ModelType = 'tensorflow'):
        """
        Initialize model wrapper
        
        Args:
            model_type: Type of model to use ('tensorflow', 'pytorch', 'huggingface')
        """
        self.model_type = model_type
        self.model = None
        self.scaler_X = StandardScaler()
        self.scaler_y = StandardScaler()
        self.feature_names = None
        self.model_path = f'backend/trained_models/model_{model_type}'
        self.scaler_path = f'backend/trained_models/scalers_{model_type}.pkl'
    
    def load_data(self):
        """Load and preprocess California housing dataset"""
        print("Loading California housing dataset...")
        housing = fetch_california_housing()
        X = housing.data
        y = housing.target.reshape(-1, 1)
        self.feature_names = housing.feature_names
        
        print(f"Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features")
        print(f"Features: {', '.join(self.feature_names)}")
        
        return X, y
    
    def preprocess_data(self, X, y):
        """Normalize features and split into train/test sets"""
        # Normalize features
        X_scaled = self.scaler_X.fit_transform(X)
        y_scaled = self.scaler_y.fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_scaled, test_size=0.2, random_state=42
        )
        
        print(f"Training set: {X_train.shape[0]} samples")
        print(f"Test set: {X_test.shape[0]} samples")
        
        return X_train, X_test, y_train, y_test
    
    def train_model(self, epochs=500, learning_rate=0.001, hidden_sizes=[64, 32, 16]):
        """
        Train the neural network model
        
        Args:
            epochs: Number of training epochs
            learning_rate: Learning rate for optimizer
            hidden_sizes: Hidden layer sizes
            
        Returns:
            Dictionary with training metrics
        """
        # Load and preprocess data
        X, y = self.load_data()
        X_train, X_test, y_train, y_test = self.preprocess_data(X, y)
        
        # Initialize model based on type
        input_size = X_train.shape[1]
        output_size = 1
        
        print(f"\n{'='*70}")
        print(f"Initializing {self.model_type.upper()} Neural Network...")
        print(f"Architecture: {input_size} -> {' -> '.join(map(str, hidden_sizes))} -> {output_size}")
        print(f"{'='*70}\n")
        
        if self.model_type == 'tensorflow':
            self.model = TensorFlowModel(
                input_size=input_size,
                hidden_sizes=hidden_sizes,
                output_size=output_size,
                learning_rate=learning_rate
            )
        elif self.model_type == 'pytorch':
            self.model = PyTorchModel(
                input_size=input_size,
                hidden_sizes=hidden_sizes,
                output_size=output_size,
                learning_rate=learning_rate
            )
        elif self.model_type == 'huggingface':
            self.model = HuggingFaceModel(
                input_size=input_size,
                hidden_sizes=hidden_sizes,
                output_size=output_size,
                learning_rate=learning_rate
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        # Display model architecture
        print("Model Architecture:")
        self.model.summary()
        
        # Train model
        print(f"\nTraining model for {epochs} epochs...")
        losses = self.model.train(X_train, y_train, epochs=epochs, batch_size=32, verbose=True)
        
        # Evaluate model
        print("\nEvaluating model...")
        train_pred = self.model.predict(X_train)
        test_pred = self.model.predict(X_test)
        
        train_r2 = calculate_r2_score(y_train, train_pred)
        test_r2 = calculate_r2_score(y_test, test_pred)
        
        # Convert back to original scale for interpretability
        train_pred_original = self.scaler_y.inverse_transform(train_pred)
        test_pred_original = self.scaler_y.inverse_transform(test_pred)
        y_train_original = self.scaler_y.inverse_transform(y_train)
        y_test_original = self.scaler_y.inverse_transform(y_test)
        
        train_mse = np.mean((y_train_original - train_pred_original) ** 2)
        test_mse = np.mean((y_test_original - test_pred_original) ** 2)
        train_rmse = np.sqrt(train_mse)
        test_rmse = np.sqrt(test_mse)
        
        print(f"\n{'='*70}")
        print(f"Training Results ({self.model_type.upper()}):")
        print(f"{'='*70}")
        print(f"  Train R² Score: {train_r2:.4f}")
        print(f"  Test R² Score: {test_r2:.4f}")
        print(f"  Train RMSE: ${train_rmse * 100000:.2f}")
        print(f"  Test RMSE: ${test_rmse * 100000:.2f}")
        print(f"{'='*70}\n")
        
        # Store metrics in model
        self.model.metrics = {
            'train_r2': float(train_r2),
            'test_r2': float(test_r2),
            'train_rmse': float(train_rmse),
            'test_rmse': float(test_rmse)
        }
        
        # Save model
        self.save_model()
        
        return {
            'losses': losses,
            'train_r2': float(train_r2),
            'test_r2': float(test_r2),
            'train_rmse': float(train_rmse),
            'test_rmse': float(test_rmse),
            'final_loss': float(losses[-1]) if losses else 0,
            'model_type': self.model_type
        }
    
    def save_model(self):
        """Save model and scalers to disk"""
        # Create trained_models directory if it doesn't exist
        os.makedirs('backend/trained_models', exist_ok=True)
        
        # Save model
        self.model.save(self.model_path)
        
        # Save scalers
        with open(self.scaler_path, 'wb') as f:
            pickle.dump({
                'scaler_X': self.scaler_X,
                'scaler_y': self.scaler_y,
                'feature_names': self.feature_names,
                'model_type': self.model_type
            }, f)
        
        print(f"\nModel saved to {self.model_path}")
        print(f"Scalers saved to {self.scaler_path}")
    
    def load_model(self):
        """Load model and scalers from disk"""
        # Check if files exist
        model_file = f"{self.model_path}.keras" if self.model_type == 'tensorflow' else f"{self.model_path}.pt"
        
        if not os.path.exists(model_file) or not os.path.exists(self.scaler_path):
            raise FileNotFoundError(f"Model files not found for {self.model_type}. Please train the model first.")
        
        # Load scalers
        with open(self.scaler_path, 'rb') as f:
            scaler_data = pickle.load(f)
            self.scaler_X = scaler_data['scaler_X']
            self.scaler_y = scaler_data['scaler_y']
            self.feature_names = scaler_data['feature_names']
        
        # Initialize and load model
        input_size = self.scaler_X.n_features_in_
        hidden_sizes = [64, 32, 16]
        
        if self.model_type == 'tensorflow':
            self.model = TensorFlowModel(input_size=input_size, hidden_sizes=hidden_sizes, output_size=1)
        elif self.model_type == 'pytorch':
            self.model = PyTorchModel(input_size=input_size, hidden_sizes=hidden_sizes, output_size=1)
        elif self.model_type == 'huggingface':
            self.model = HuggingFaceModel(input_size=input_size, hidden_sizes=hidden_sizes, output_size=1)
        
        self.model.load(self.model_path)
        
        print(f"{self.model_type.upper()} model loaded successfully")
    
    def predict(self, features):
        """
        Make prediction for given house features
        
        Args:
            features: Dictionary with feature names and values or numpy array
        
        Returns:
            Predicted house price
        """
        if self.model is None:
            self.load_model()
        
        # Convert dictionary to array if needed
        if isinstance(features, dict):
            feature_array = np.array([[
                features.get('MedInc', 3.0),
                features.get('HouseAge', 25.0),
                features.get('AveRooms', 5.0),
                features.get('AveBedrms', 1.0),
                features.get('Population', 1500.0),
                features.get('AveOccup', 3.0),
                features.get('Latitude', 35.0),
                features.get('Longitude', -120.0)
            ]])
        else:
            feature_array = features.reshape(1, -1) if features.ndim == 1 else features
        
        # Scale features
        features_scaled = self.scaler_X.transform(feature_array)
        
        # Predict
        prediction_scaled = self.model.predict(features_scaled)
        
        # Inverse transform to get actual price
        prediction = self.scaler_y.inverse_transform(prediction_scaled)
        
        return float(prediction[0][0])


def train_all_models(epochs=500, learning_rate=0.001):
    """
    Train all three model types for comparison
    
    Args:
        epochs: Number of training epochs
        learning_rate: Learning rate
        
    Returns:
        Dictionary with metrics for all models
    """
    results = {}
    
    for model_type in ['tensorflow', 'pytorch', 'huggingface']:
        print(f"\n\n{'#'*70}")
        print(f"# Training {model_type.upper()} Model")
        print(f"{'#'*70}\n")
        
        model = HousePriceModel(model_type=model_type)
        metrics = model.train_model(epochs=epochs, learning_rate=learning_rate)
        results[model_type] = metrics
    
    # Print comparison
    print(f"\n\n{'='*70}")
    print("MODEL COMPARISON SUMMARY")
    print(f"{'='*70}")
    print(f"{'Model':<20} {'Test R²':<12} {'Test RMSE':<15} {'Final Loss':<12}")
    print(f"{'-'*70}")
    
    for model_type, metrics in results.items():
        print(f"{model_type.upper():<20} {metrics['test_r2']:<12.4f} "
              f"${metrics['test_rmse']*100000:<14,.2f} {metrics['final_loss']:<12.6f}")
    
    print(f"{'='*70}\n")
    
    return results


if __name__ == "__main__":
    import sys
    
    # Check if specific model type is requested
    if len(sys.argv) > 1:
        model_type = sys.argv[1].lower()
        if model_type in ['tensorflow', 'pytorch', 'huggingface']:
            model = HousePriceModel(model_type=model_type)
            metrics = model.train_model(epochs=500, learning_rate=0.001)
        elif model_type == 'all':
            results = train_all_models(epochs=500, learning_rate=0.001)
        else:
            print(f"Unknown model type: {model_type}")
            print("Usage: python train.py [tensorflow|pytorch|huggingface|all]")
    else:
        # Default: train TensorFlow model
        print("Training TensorFlow model (default)")
        print("Use 'python train.py all' to train all models")
        model = HousePriceModel(model_type='tensorflow')
        metrics = model.train_model(epochs=500, learning_rate=0.001)
    
    print("\n" + "="*50)
    print("Training Complete!")
    print("="*50)
