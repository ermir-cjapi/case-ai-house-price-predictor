"""
Command-line interface for model training
Provides easy access to train models without starting the API server
"""
from services.training_service import HousePriceModel, train_all_models

# Re-export for backward compatibility
__all__ = ['HousePriceModel', 'train_all_models']

if __name__ == "__main__":
    import sys
    
    # Check if specific model type is requested
    if len(sys.argv) > 1:
        model_type = sys.argv[1].lower()
        if model_type in ['tensorflow', 'pytorch', 'xgboost']:
            model = HousePriceModel(model_type=model_type)
            metrics = model.train_model(epochs=500, learning_rate=0.001)
        elif model_type == 'all':
            results = train_all_models(epochs=500, learning_rate=0.001)
        else:
            print(f"Unknown model type: {model_type}")
            print("Usage: python train_cli.py [tensorflow|pytorch|xgboost|all]")
    else:
        # Default: train TensorFlow model
        print("Training TensorFlow model (default)")
        print("Use 'python train_cli.py all' to train all models")
        model = HousePriceModel(model_type='tensorflow')
        metrics = model.train_model(epochs=500, learning_rate=0.001)
    
    print("\n" + "="*50)
    print("Training Complete!")
    print("="*50)
