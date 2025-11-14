"""
TabPFN Zero-Shot Tabular Regressor for house price prediction
Uses pretrained TabPFN model - NO TRAINING/FINE-TUNING NEEDED!

TabPFN is a transformer pretrained on millions of synthetic tabular datasets,
enabling it to make accurate predictions on new tabular data in a single forward pass.
"""
import numpy as np
from tabpfn import TabPFNRegressor
import pickle
from typing import List
from .base_model import BaseHousingModel


class HuggingFaceModel(BaseHousingModel):
    """
    TabPFN Zero-Shot Model for house price prediction
    
    This model uses TabPFN (Tabular Prior-data Fitted Network), a transformer
    pretrained on millions of synthetic tabular datasets. It can make predictions
    on NEW tabular data WITHOUT any training or fine-tuning!
    
    Key Benefits:
    - Zero-shot: No training required
    - Fast: Instant predictions after fit
    - Accurate: Pretrained on diverse tabular patterns
    - Simple: Scikit-learn-like interface
    
    How it works:
    1. TabPFN was pretrained on millions of synthetic tabular regression problems
    2. It learned general patterns of how features relate to targets
    3. On your data, it uses "in-context learning" - like GPT for tabular data
    4. The fit() method just stores your data, no actual training happens
    5. predict() uses the pretrained model to make predictions
    """
    
    def __init__(self, input_size=8, hidden_sizes=None, output_size=1, 
                 learning_rate=0.001, n_estimators=4):
        """
        Initialize TabPFN model
        
        Args:
            input_size: Number of input features (for compatibility)
            hidden_sizes: Not used, kept for compatibility with base class
            output_size: Number of outputs (for compatibility)
            learning_rate: Not used (no training needed!)
            n_estimators: Number of ensemble members (default: 4)
        """
        super().__init__(input_size, hidden_sizes or [768], output_size, learning_rate)
        
        print("Initializing TabPFN Zero-Shot Regressor...")
        print("⚡ This model requires NO TRAINING - it's already pretrained!")
        
        # Initialize TabPFN regressor
        # n_estimators: number of ensemble members (4 is recommended)
        self.model = TabPFNRegressor(
            N_ensemble_configurations=n_estimators,
            device='cpu'  # Can use 'cuda' if GPU available
        )
        
        # Storage for training data (used by TabPFN for in-context learning)
        self.X_train = None
        self.y_train = None
        self.is_fitted = False
        
        print("✓ TabPFN model initialized successfully")
    
    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 500, 
              batch_size: int = 32, verbose: bool = True) -> List[float]:
        """
        'Train' the TabPFN model (actually just fits/stores the data)
        
        NOTE: TabPFN doesn't actually train! The pretrained model uses
        in-context learning similar to GPT. This method just stores your
        data for the model to use as context.
        
        Args:
            X: Training features
            y: Training labels
            epochs: Not used (kept for compatibility)
            batch_size: Not used (kept for compatibility)
            verbose: Print progress
            
        Returns:
            Empty list (no training losses since no training happens)
        """
        if verbose:
            print("\n" + "="*70)
            print("TabPFN Zero-Shot Learning")
            print("="*70)
            print("⚡ TabPFN is PRETRAINED - no training needed!")
            print("📊 Fitting data for in-context learning...")
            print(f"   Training samples: {X.shape[0]}")
            print(f"   Features: {X.shape[1]}")
        
        # Reshape y if needed (TabPFN expects 1D)
        if y.ndim > 1:
            y = y.ravel()
        
        # Store data and fit (this is instant, no training!)
        self.X_train = X
        self.y_train = y
        
        try:
            # TabPFN fit is instant - it just stores the data
            self.model.fit(X, y)
            self.is_fitted = True
            
            if verbose:
                print("✓ Data fitted successfully!")
                print("✓ Model ready for zero-shot predictions")
                print("="*70 + "\n")
            
        except Exception as e:
            print(f"❌ Error during fit: {e}")
            print("Note: TabPFN works best with datasets < 10k rows and < 100 features")
            raise
        
        # Return empty list (no training losses)
        return []
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make zero-shot predictions using pretrained TabPFN
        
        Args:
            X: Input features
            
        Returns:
            Predictions as numpy array
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted! Call train() first to fit the data.")
        
        # Make predictions (this uses the pretrained model!)
        predictions = self.model.predict(X)
        
        # Reshape to match expected format
        if predictions.ndim == 1:
            predictions = predictions.reshape(-1, 1)
        
        return predictions
    
    def save(self, filepath: str) -> None:
        """
        Save fitted model to disk
        
        Args:
            filepath: Path to save the model
        """
        if filepath.endswith('.pkl'):
            filepath = filepath[:-4]
        
        # Save the fitted data and model state
        save_data = {
            'X_train': self.X_train,
            'y_train': self.y_train,
            'is_fitted': self.is_fitted,
            'input_size': self.input_size,
            'hidden_sizes': self.hidden_sizes,
            'output_size': self.output_size,
            'learning_rate': self.learning_rate,
            'model_type': 'tabpfn_zeroshot'
        }
        
        with open(f"{filepath}.pt", 'wb') as f:
            pickle.dump(save_data, f)
        
        # Save metadata
        metadata = {
            'input_size': self.input_size,
            'hidden_sizes': self.hidden_sizes,
            'output_size': self.output_size,
            'learning_rate': self.learning_rate,
            'model_type': 'tabpfn_zeroshot',
            'is_fitted': self.is_fitted
        }
        with open(f"{filepath}_metadata.pkl", 'wb') as f:
            pickle.dump(metadata, f)
        
        print(f"✓ TabPFN model saved to {filepath}.pt")
    
    def load(self, filepath: str) -> None:
        """
        Load fitted model from disk
        
        Args:
            filepath: Path to load the model from
        """
        if filepath.endswith('.pkl'):
            filepath = filepath[:-4]
        
        # Load saved data
        with open(f"{filepath}.pt", 'rb') as f:
            save_data = pickle.load(f)
        
        self.X_train = save_data['X_train']
        self.y_train = save_data['y_train']
        self.is_fitted = save_data['is_fitted']
        self.input_size = save_data['input_size']
        self.hidden_sizes = save_data['hidden_sizes']
        self.output_size = save_data['output_size']
        self.learning_rate = save_data['learning_rate']
        
        # Re-initialize and fit the model
        self.model = TabPFNRegressor(device='cpu')
        if self.is_fitted:
            self.model.fit(self.X_train, self.y_train)
        
        print(f"✓ TabPFN model loaded from {filepath}.pt")
    
    def summary(self) -> None:
        """Print model summary"""
        print("\n" + "="*70)
        print("TabPFN Zero-Shot Tabular Regressor")
        print("="*70)
        print("Model Type: TabPFN (Tabular Prior-data Fitted Network)")
        print("Training Required: ❌ NO - Pretrained on millions of datasets!")
        print("="*70)
        
        print("\nModel Details:")
        print(f"  • Pretrained: ✓ Yes (on millions of synthetic tabular datasets)")
        print(f"  • Training needed: ✗ No")
        print(f"  • Learning type: In-context learning (like GPT for tabular data)")
        print(f"  • Fitted: {'✓ Yes' if self.is_fitted else '✗ Not yet'}")
        
        if self.is_fitted:
            print(f"\nFitted Data:")
            print(f"  • Training samples: {self.X_train.shape[0]:,}")
            print(f"  • Features: {self.X_train.shape[1]}")
        
        print("\nCapabilities:")
        print("  • Zero-shot predictions: ✓")
        print("  • Handles numerical features: ✓")
        print("  • Handles categorical features: ✓")
        print("  • Handles missing values: ✓")
        print("  • Best for: Small-medium datasets (< 10k rows, < 100 features)")
        
        print("\nHow it works:")
        print("  1. TabPFN was pretrained on millions of synthetic datasets")
        print("  2. It learned general patterns of tabular data relationships")
        print("  3. On YOUR data, it uses in-context learning")
        print("  4. No training/fine-tuning required!")
        
        print("="*70 + "\n")
    
    def get_param_count(self) -> int:
        """
        Get parameter count
        
        Note: TabPFN has ~50M parameters but they're all pretrained.
        You don't train any parameters!
        """
        return 0  # 0 trainable params (all pretrained!)


# For backward compatibility with old code
class HuggingFaceTabularModel:
    """Deprecated - use HuggingFaceModel instead"""
    def __init__(self, *args, **kwargs):
        raise DeprecationWarning(
            "HuggingFaceTabularModel is deprecated. "
            "The new implementation uses TabPFN directly through HuggingFaceModel."
        )
