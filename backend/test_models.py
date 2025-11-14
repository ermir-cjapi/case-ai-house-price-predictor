"""
Test script for all three models
Verifies that each model can train and make predictions
"""
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from models.tensorflow_model import TensorFlowModel
from models.pytorch_model import PyTorchModel
from models.xgboost_model import XGBoostModel
from models.base_model import calculate_r2_score
from router.langgraph_router import create_model_router
from router.model_selector import select_model_by_criteria, get_model_characteristics

def test_data_loading():
    """Test data loading and preprocessing"""
    print("="*70)
    print("TEST 1: Data Loading")
    print("="*70)
    
    housing = fetch_california_housing()
    X = housing.data
    y = housing.target.reshape(-1, 1)
    
    assert X.shape[0] == 20640, "Expected 20,640 samples"
    assert X.shape[1] == 8, "Expected 8 features"
    
    print(f"✓ Loaded {X.shape[0]} samples with {X.shape[1]} features")
    print(f"✓ Target shape: {y.shape}")
    print("PASSED\n")
    
    return X, y


def test_model_initialization(model_class, model_name):
    """Test model initialization"""
    print(f"Testing {model_name} initialization...")
    
    model = model_class(
        input_size=8,
        hidden_sizes=[64, 32, 16],
        output_size=1,
        learning_rate=0.001
    )
    
    print(f"✓ {model_name} initialized successfully")
    
    # Test summary
    print(f"✓ Model summary:")
    model.summary()
    
    return model


def test_model_training(model, X, y, model_name):
    """Test model training"""
    print(f"\nTesting {model_name} training...")
    
    # Use smaller dataset for quick testing
    X_small = X[:1000]
    y_small = y[:1000]
    
    # Normalize
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()
    X_scaled = scaler_X.fit_transform(X_small)
    y_scaled = scaler_y.fit_transform(y_small)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_scaled, test_size=0.2, random_state=42
    )
    
    # Train for just 50 epochs for quick test
    losses = model.train(X_train, y_train, epochs=50, batch_size=32, verbose=False)
    
    print(f"✓ {model_name} trained for 50 epochs")
    print(f"✓ Initial loss: {losses[0]:.4f}")
    print(f"✓ Final loss: {losses[-1]:.4f}")
    print(f"✓ Loss decreased: {losses[0] > losses[-1]}")
    
    # Test prediction
    predictions = model.predict(X_test)
    r2 = calculate_r2_score(y_test, predictions)
    
    print(f"✓ Test R² score: {r2:.4f}")
    
    assert len(predictions) == len(X_test), "Prediction count mismatch"
    assert r2 > 0.5, f"R² score too low: {r2}"
    
    print(f"✓ {model_name} PASSED\n")
    
    return model


def test_model_save_load(model, model_name):
    """Test model save and load"""
    print(f"Testing {model_name} save/load...")
    
    # Save
    filepath = f'backend/data/test_{model_name.lower()}'
    model.save(filepath)
    print(f"✓ {model_name} saved to {filepath}")
    
    # Create new instance and load
    if 'TensorFlow' in model_name:
        new_model = TensorFlowModel(input_size=8, hidden_sizes=[64, 32, 16], output_size=1)
    elif 'PyTorch' in model_name:
        new_model = PyTorchModel(input_size=8, hidden_sizes=[64, 32, 16], output_size=1)
    else:
        new_model = XGBoostModel(input_size=8, hidden_sizes=[64, 32, 16], output_size=1)
    
    new_model.load(filepath)
    print(f"✓ {model_name} loaded successfully")
    
    # Test that loaded model can predict
    test_input = np.random.randn(5, 8)
    predictions = new_model.predict(test_input)
    assert predictions.shape == (5, 1), "Loaded model prediction shape mismatch"
    
    print(f"✓ Loaded model can make predictions")
    print(f"✓ {model_name} save/load PASSED\n")


def test_langgraph_router():
    """Test LangGraph router"""
    print("="*70)
    print("TEST: LangGraph Router")
    print("="*70)
    
    router = create_model_router()
    print("✓ Router created successfully")
    
    # Test different routing scenarios
    test_cases = [
        {'preference': 'auto', 'criteria': {'priority': 'speed'}, 'expected': 'pytorch'},
        {'preference': 'auto', 'criteria': {'priority': 'accuracy'}, 'expected': 'tensorflow'},
        {'preference': 'auto', 'criteria': {'priority': 'experimental'}, 'expected': 'xgboost'},
        {'preference': 'tensorflow', 'criteria': {}, 'expected': 'tensorflow'},
        {'preference': 'ensemble', 'criteria': {}, 'expected': 'ensemble'},
    ]
    
    features = {
        'MedInc': 3.5,
        'HouseAge': 25.0,
        'AveRooms': 5.0,
        'AveBedrms': 1.0,
        'Population': 1500.0,
        'AveOccup': 3.0,
        'Latitude': 35.0,
        'Longitude': -120.0
    }
    
    for i, test_case in enumerate(test_cases, 1):
        result = router.route(
            features=features,
            model_preference=test_case['preference'],
            criteria=test_case['criteria']
        )
        
        assert result['selected_model'] == test_case['expected'], \
            f"Test case {i} failed: expected {test_case['expected']}, got {result['selected_model']}"
        
        print(f"✓ Test case {i}: {test_case['preference']} with {test_case['criteria']} → {result['selected_model']}")
    
    print("✓ All routing tests PASSED\n")


def test_model_characteristics():
    """Test model characteristics retrieval"""
    print("="*70)
    print("TEST: Model Characteristics")
    print("="*70)
    
    characteristics = get_model_characteristics()
    
    expected_models = ['tensorflow', 'pytorch', 'xgboost', 'ensemble']
    
    for model_type in expected_models:
        assert model_type in characteristics, f"{model_type} missing from characteristics"
        
        char = characteristics[model_type]
        assert 'name' in char, f"{model_type} missing 'name'"
        assert 'architecture' in char, f"{model_type} missing 'architecture'"
        assert 'strengths' in char, f"{model_type} missing 'strengths'"
        
        print(f"✓ {model_type}: {char['name']}")
    
    print("✓ All characteristics present")
    print("✓ Model characteristics test PASSED\n")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print(" MULTI-MODEL NEURAL NETWORK TEST SUITE")
    print("="*70 + "\n")
    
    try:
        # Test 1: Data loading
        X, y = test_data_loading()
        
        # Test 2: Model characteristics
        test_model_characteristics()
        
        # Test 3: LangGraph router
        test_langgraph_router()
        
        # Test 4-6: Each model
        models_to_test = [
            (TensorFlowModel, "TensorFlow"),
            (PyTorchModel, "PyTorch"),
            (XGBoostModel, "XGBoost")
        ]
        
        for model_class, model_name in models_to_test:
            print("="*70)
            print(f"TEST: {model_name} Model")
            print("="*70)
            
            # Initialize
            model = test_model_initialization(model_class, model_name)
            
            # Train
            model = test_model_training(model, X, y, model_name)
            
            # Save/Load
            test_model_save_load(model, model_name)
        
        # Summary
        print("="*70)
        print(" ALL TESTS PASSED! ✓")
        print("="*70)
        print("\nSummary:")
        print("✓ Data loading and preprocessing")
        print("✓ Model characteristics")
        print("✓ LangGraph routing")
        print("✓ TensorFlow model (init, train, save/load)")
        print("✓ PyTorch model (init, train, save/load)")
        print("✓ Transformer model (init, train, save/load)")
        print("\nAll systems operational! 🚀")
        
        return True
        
    except Exception as e:
        print("\n" + "="*70)
        print(" TEST FAILED ✗")
        print("="*70)
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

