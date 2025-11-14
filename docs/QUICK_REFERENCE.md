# Quick Reference Guide

## 🚀 Fast Commands

### Training Models

```bash
# Train TensorFlow model
python backend/train.py tensorflow

# Train PyTorch model
python backend/train.py pytorch

# Train Transformer model
python backend/train.py huggingface

# Train ALL models (recommended)
python backend/train.py all
```

### Starting the Application

```bash
# Backend (Terminal 1)
cd backend
python api.py

# Frontend (Terminal 2)
cd frontend
npm run dev
```

### Making Predictions (API)

```bash
# Auto mode (LangGraph decides)
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{
  "sqft": 1500, "bedrooms": 3, "bathrooms": 2,
  "latitude": 34.05, "longitude": -118.25,
  "model_preference": "auto",
  "criteria": {"priority": "accuracy"}
}'

# Specific model
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{
  "sqft": 1500, "bedrooms": 3, "bathrooms": 2,
  "latitude": 34.05, "longitude": -118.25,
  "model_preference": "pytorch"
}'

# Ensemble (all 3 models)
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{
  "sqft": 1500, "bedrooms": 3, "bathrooms": 2,
  "latitude": 34.05, "longitude": -118.25,
  "model_preference": "ensemble"
}'
```

## 🎯 Model Selection Guide

| Your Goal | Select | Why |
|-----------|--------|-----|
| Fastest predictions | PyTorch | Optimized inference |
| Most reliable | TensorFlow | Production-proven |
| Learn transformers | Transformer | Educational value |
| Best accuracy | Ensemble | Combines all 3 |

## 📍 Important URLs

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:5000/docs
- **API RedDocs**: http://localhost:5000/redoc
- **Health**: http://localhost:5000/health

## 🔧 Key API Endpoints

```bash
GET  /health                    # Check API status
GET  /models/status             # Check trained models
GET  /models/characteristics    # Get model info
POST /train/{model_type}        # Train model
POST /predict                   # Predict with routing
POST /predict/compare           # Compare all models
```

## 📊 Model Architectures

### TensorFlow & PyTorch
```
8 inputs → 64 → 32 → 16 → 1 output
Parameters: 3,201
```

### Transformer
```
8 inputs → Projection → 2x Transformer → 1 output
Parameters: ~15,000
```

## 💡 LangGraph Routing Logic

```
Priority = "speed"        → PyTorch
Priority = "accuracy"     → TensorFlow
Priority = "experimental" → Transformer
Priority = "balanced"     → Ensemble
```

## 🐛 Quick Troubleshooting

### Backend won't start
```bash
cd backend
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Model not found
```bash
python backend/train.py tensorflow  # Train at least one model
```

### Port already in use
```bash
# Change port in api.py:
port = int(os.environ.get('PORT', 5001))  # Use 5001 instead
```

## 📦 File Locations

- **Models**: `backend/data/model_[type].keras` or `.pt`
- **Scalers**: `backend/data/scalers_[type].pkl`
- **Logs**: Console output only (add logging if needed)

## 🧪 Testing

```bash
# Run test suite
cd backend
python test_models.py
```

## 📚 Documentation

- **Full Comparison**: `MODEL_COMPARISON.md`
- **Setup Guide**: `SETUP_GUIDE.md`
- **This Reference**: `QUICK_REFERENCE.md`
- **Implementation Status**: `IMPLEMENTATION_COMPLETE.md`

## 🎓 Learning Path

1. **Start**: Train TensorFlow model → Make predictions
2. **Compare**: Train all 3 → Compare results
3. **Explore**: Try different architectures/parameters
4. **Advanced**: Modify routing logic, add new models

## ⚡ Performance Expectations

### Training (CPU, 500 epochs)
- TensorFlow: ~75 seconds
- PyTorch: ~60 seconds
- Transformer: ~125 seconds

### Accuracy (Test R²)
- All models: ~0.80
- Ensemble: ~0.81

### Inference Speed
- PyTorch: ~1ms (fastest)
- TensorFlow: ~2ms
- Transformer: ~5ms

## 🔑 Key Concepts

- **Auto Mode**: LangGraph selects model based on criteria
- **Ensemble**: Averages predictions from all 3 models
- **Routing**: Decision graph picks optimal model
- **R² Score**: 1.0 = perfect, 0.8 = good for this dataset

## 💻 Development Tips

### Add New Model
1. Inherit from `BaseHousingModel`
2. Implement required methods
3. Add to `train.py` and `api.py`
4. Update router logic

### Modify Architecture
```python
# In train.py or directly:
hidden_sizes = [128, 64, 32]  # Larger network
learning_rate = 0.0001         # Slower learning
epochs = 1000                  # More training
```

### Custom Routing
Edit `backend/router/model_selector.py`:
```python
def select_model_by_criteria(preference, criteria):
    # Add your logic here
    if criteria.get("custom_condition"):
        return "your_model"
```

## 🎯 Common Use Cases

### Research
```bash
# Train with different parameters
python backend/train.py pytorch --epochs 1000 --lr 0.0001
```

### Production
```bash
# Use TensorFlow for stability
model_preference = "tensorflow"
```

### Learning
```bash
# Try transformer architecture
model_preference = "huggingface"
```

### Critical Applications
```bash
# Use ensemble for best results
model_preference = "ensemble"
```

---

**Need more details?** Check the full documentation files! 📖

