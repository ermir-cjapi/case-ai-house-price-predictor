"""
XGBoost Model for house price prediction
Uses gradient boosting - one of the best algorithms for tabular data!

XGBoost (Extreme Gradient Boosting) is a powerful, efficient implementation
of gradient boosting that consistently wins machine learning competitions.
"""
import numpy as np
import xgboost as xgb
import pickle
from typing import List
from .base_model import BaseHousingModel


class XGBoostModel(BaseHousingModel):
    """
    XGBoost Model for house price prediction
    
    XGBoost is one of the most effective algorithms for tabular data:
    - Fast training
    - High accuracy
    - Built-in regularization
    - Handles various data types
    - Industry standard for structured data
    
    XGBoost uses gradient boosting on decision trees, making it perfect
    for tabular regression tasks like house price prediction.
    """
    
    def __init__(self, input_size=8, hidden_sizes=None, output_size=1, 
                 learning_rate=0.1, n_estimators=100):
        """
        Initialize XGBoost model
        
        Args:
            input_size: Number of input features (for compatibility)
            hidden_sizes: Not used, kept for compatibility with base class
            output_size: Number of outputs (for compatibility)
            learning_rate: Learning rate (default: 0.1, typical for XGBoost)
            n_estimators: Number of boosting rounds/trees (default: 100)
        """
        super().__init__(input_size, hidden_sizes or [768], output_size, learning_rate)
        
        print("Initializing XGBoost Regressor...")
        print("🌳 XGBoost: The gold standard for tabular data!")
        
        self.n_estimators = n_estimators
        
        # XGBoost parameters - optimized for regression
        self.params = {
            'objective': 'reg:squarederror',  # Regression with MSE
            'learning_rate': learning_rate,
            'max_depth': 6,  # Tree depth
            'min_child_weight': 1,
            'subsample': 0.8,  # Row sampling
            'colsample_bytree': 0.8,  # Column sampling
            'reg_alpha': 0.1,  # L1 regularization
            'reg_lambda': 1.0,  # L2 regularization
            'random_state': 42,
            'n_jobs': -1,  # Use all CPU cores
            'verbosity': 0  # Quiet mode
        }
        
        self.model = None
        self.is_fitted = False
        
        print("✓ XGBoost initialized successfully")
        print(f"  • Trees: {n_estimators}")
        print(f"  • Learning rate: {learning_rate}")
        print(f"  • Max depth: 6")
    
    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 100, 
              batch_size: int = 32, verbose: bool = True) -> List[float]:
        """
        Train XGBoost model
        
        Note: XGBoost uses boosting rounds instead of epochs.
        The epochs parameter is mapped to n_estimators (number of trees).
        
        Args:
            X: Training features
            y: Training labels
            epochs: Number of boosting rounds (maps to n_estimators)
            batch_size: Not used by XGBoost (kept for compatibility)
            verbose: Print training progress
            
        Returns:
            List of training losses (one per boosting round)
        """
        if verbose:
            print("\n" + "="*70)
            print("XGBoost Gradient Boosting")
            print("="*70)
            print("🌳 Training ensemble of gradient-boosted trees")
            print(f"   Training samples: {X.shape[0]}")
            print(f"   Features: {X.shape[1]}")
            print(f"   Boosting rounds: {epochs}")
            print(f"   Learning rate: {self.learning_rate}")
        
        # Reshape y if needed
        if y.ndim > 1:
            y = y.ravel()
        
        # Create DMatrix (XGBoost's internal data structure)
        dtrain = xgb.DMatrix(X, label=y)
        
        # Store evaluation results
        evals_result = {}
        
        try:
            if verbose:
                print(f"\n🚀 Training XGBoost model...")
                # Train with progress
                self.model = xgb.train(
                    params=self.params,
                    dtrain=dtrain,
                    num_boost_round=epochs,
                    evals=[(dtrain, 'train')],
                    evals_result=evals_result,
                    verbose_eval=max(1, epochs // 10)  # Print every 10%
                )
            else:
                # Train quietly
                self.params['verbosity'] = 0
                self.model = xgb.train(
                    params=self.params,
                    dtrain=dtrain,
                    num_boost_round=epochs,
                    evals=[(dtrain, 'train')],
                    evals_result=evals_result,
                    verbose_eval=False
                )
            
            self.is_fitted = True
            
            if verbose:
                final_rmse = evals_result['train']['rmse'][-1]
                print(f"\n✓ XGBoost training complete!")
                print(f"✓ Final training RMSE: {final_rmse:.4f}")
                print("="*70 + "\n")
            
        except Exception as e:
            print(f"❌ Error during training: {e}")
            raise
        
        # Return RMSE values as "losses"
        return evals_result.get('train', {}).get('rmse', [])
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions using trained XGBoost model
        
        Args:
            X: Input features
            
        Returns:
            Predictions as numpy array
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted! Call train() first.")
        
        # Create DMatrix for prediction
        dtest = xgb.DMatrix(X)
        
        # Make predictions
        predictions = self.model.predict(dtest)
        
        # Reshape to match expected format
        if predictions.ndim == 1:
            predictions = predictions.reshape(-1, 1)
        
        return predictions
    
    def save(self, filepath: str) -> None:
        """
        Save trained model to disk
        
        Args:
            filepath: Path to save the model
        """
        if filepath.endswith('.pkl'):
            filepath = filepath[:-4]
        
        # Save XGBoost model
        if self.model:
            self.model.save_model(f"{filepath}.json")
        
        # Save metadata
        metadata = {
            'input_size': self.input_size,
            'hidden_sizes': self.hidden_sizes,
            'output_size': self.output_size,
            'learning_rate': self.learning_rate,
            'n_estimators': self.n_estimators,
            'params': self.params,
            'model_type': 'xgboost',
            'is_fitted': self.is_fitted
        }
        with open(f"{filepath}_metadata.pkl", 'wb') as f:
            pickle.dump(metadata, f)
        
        print(f"✓ XGBoost model saved to {filepath}.json")
    
    def load(self, filepath: str) -> None:
        """
        Load trained model from disk
        
        Args:
            filepath: Path to load the model from
        """
        if filepath.endswith('.pkl'):
            filepath = filepath[:-4]
        
        # Load metadata
        with open(f"{filepath}_metadata.pkl", 'rb') as f:
            metadata = pickle.load(f)
        
        self.input_size = metadata['input_size']
        self.hidden_sizes = metadata['hidden_sizes']
        self.output_size = metadata['output_size']
        self.learning_rate = metadata['learning_rate']
        self.n_estimators = metadata.get('n_estimators', 100)
        self.params = metadata.get('params', self.params)
        self.is_fitted = metadata['is_fitted']
        
        # Load XGBoost model
        if self.is_fitted:
            self.model = xgb.Booster()
            self.model.load_model(f"{filepath}.json")
        
        print(f"✓ XGBoost model loaded from {filepath}.json")
    
    def summary(self) -> None:
        """Print model summary"""
        print("\n" + "="*70)
        print("XGBoost Gradient Boosting Model")
        print("="*70)
        print("Algorithm: Extreme Gradient Boosting")
        print("Type: Ensemble of decision trees")
        print("="*70)
        
        print("\nModel Configuration:")
        print(f"  • Number of trees: {self.n_estimators}")
        print(f"  • Learning rate: {self.learning_rate}")
        print(f"  • Max depth: {self.params['max_depth']}")
        print(f"  • Subsample: {self.params['subsample']}")
        print(f"  • Column sample: {self.params['colsample_bytree']}")
        print(f"  • L1 regularization: {self.params['reg_alpha']}")
        print(f"  • L2 regularization: {self.params['reg_lambda']}")
        
        print(f"\nStatus:")
        print(f"  • Fitted: {'✓ Yes' if self.is_fitted else '✗ Not yet'}")
        
        if self.is_fitted and self.model:
            print(f"  • Actual trees trained: {self.model.num_boosted_rounds()}")
        
        print("\nKey Features:")
        print("  • Fast training: ✓")
        print("  • High accuracy: ✓")
        print("  • Handles missing values: ✓")
        print("  • Built-in regularization: ✓")
        print("  • Parallel processing: ✓")
        print("  • Industry standard: ✓")
        
        print("\nWhy XGBoost for Tabular Data:")
        print("  • Consistently wins ML competitions")
        print("  • Optimized for structured/tabular data")
        print("  • Better than neural networks for many tasks")
        print("  • Fast inference")
        print("  • Easy to tune")
        
        print("="*70 + "\n")
    
    def get_param_count(self) -> int:
        """
        Get number of trees (XGBoost's version of parameters)
        
        Note: Each tree has many split nodes, so actual parameter
        count is trees * avg_nodes_per_tree
        """
        if self.is_fitted and self.model:
            return self.model.num_boosted_rounds()
        return 0


# For backward compatibility
class HuggingFaceModel:
    """Deprecated - use XGBoostModel instead"""
    def __init__(self, *args, **kwargs):
        import warnings
        warnings.warn(
            "HuggingFaceModel is deprecated and renamed to XGBoostModel. "
            "Please update your imports: from models.xgboost_model import XGBoostModel",
            DeprecationWarning,
            stacklevel=2
        )
        # Redirect to the new class
        from models.xgboost_model import XGBoostModel
        self.__class__ = XGBoostModel
        XGBoostModel.__init__(self, *args, **kwargs)
