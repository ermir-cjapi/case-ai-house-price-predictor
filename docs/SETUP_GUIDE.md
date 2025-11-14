# Multi-Model Neural Network Setup Guide

## Quick Start

This guide will help you set up and run the multi-model house price prediction system with TensorFlow, PyTorch, and Transformer models.

## Prerequisites

- **Python**: 3.9 - 3.11
- **Node.js**: 16+ and npm
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 2GB free space

## Installation Steps

### 1. Clone the Repository

```bash
cd ai-deep-learning-example
```

### 2. Backend Setup

#### Option A: Windows

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Option B: Linux/Mac

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend (from project root)
cd frontend

# Install dependencies
npm install
```

## Running the Application

### Method 1: Using Provided Scripts (Recommended)

#### Windows

```powershell
# Terminal 1: Start backend
.\start-backend.bat

# Terminal 2: Start frontend
.\start-frontend.bat
```

#### Linux/Mac

```bash
# Terminal 1: Start backend
./start-backend.sh

# Terminal 2: Start frontend
./start-frontend.sh
```

### Method 2: Manual Start

#### Backend

```bash
cd backend
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
python api.py
```

Backend will run on: `http://localhost:5000`

#### Frontend

```bash
cd frontend
npm run dev
```

Frontend will run on: `http://localhost:3000`

## Training Models

### Option 1: Via Web Interface

1. Open `http://localhost:3000` in your browser
2. Navigate to the Training Panel
3. Click "Train Model" (trains TensorFlow by default)

### Option 2: Via Command Line

```bash
cd backend
source venv/bin/activate  # Activate venv first

# Train specific model
python train.py tensorflow
python train.py pytorch
python train.py huggingface

# Train all models at once (recommended)
python train.py all
```

### Option 3: Via API

```bash
# Train TensorFlow model
curl -X POST http://localhost:5000/train/tensorflow \
  -H "Content-Type: application/json" \
  -d '{"epochs": 500, "learning_rate": 0.001}'

# Train PyTorch model
curl -X POST http://localhost:5000/train/pytorch \
  -H "Content-Type: application/json" \
  -d '{"epochs": 500}'

# Train Transformer model
curl -X POST http://localhost:5000/train/huggingface \
  -H "Content-Type: application/json" \
  -d '{"epochs": 500}'

# Train all models
curl -X POST http://localhost:5000/train/all \
  -H "Content-Type: application/json" \
  -d '{"epochs": 500}'
```

## Making Predictions

### Via Web Interface

1. Ensure at least one model is trained
2. Enter house details in the prediction form
3. Select model preference (or use Auto mode)
4. Click "Predict Price"

### Via API

```bash
# Auto mode (LangGraph decides)
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sqft": 1500,
    "bedrooms": 3,
    "bathrooms": 2,
    "latitude": 34.05,
    "longitude": -118.25,
    "median_income": 3.5,
    "house_age": 25,
    "population": 1500,
    "model_preference": "auto",
    "criteria": {"priority": "accuracy"}
  }'

# Specific model
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sqft": 1500,
    "bedrooms": 3,
    "bathrooms": 2,
    "latitude": 34.05,
    "longitude": -118.25,
    "model_preference": "pytorch"
  }'

# Ensemble (all 3 models)
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sqft": 1500,
    "bedrooms": 3,
    "bathrooms": 2,
    "latitude": 34.05,
    "longitude": -118.25,
    "model_preference": "ensemble"
  }'

# Compare all models
curl -X POST http://localhost:5000/predict/compare \
  -H "Content-Type: application/json" \
  -d '{
    "sqft": 1500,
    "bedrooms": 3,
    "bathrooms": 2,
    "latitude": 34.05,
    "longitude": -118.25
  }'
```

## API Endpoints

### Health & Status

```bash
# Health check
GET http://localhost:5000/health

# Model status
GET http://localhost:5000/models/status

# Model characteristics
GET http://localhost:5000/models/characteristics
```

### Training

```bash
# Train specific model
POST http://localhost:5000/train/{model_type}
# model_type: tensorflow, pytorch, huggingface, all

Body:
{
  "epochs": 500,
  "learning_rate": 0.001,
  "hidden_sizes": [64, 32, 16]
}
```

### Prediction

```bash
# Single prediction with routing
POST http://localhost:5000/predict

Body:
{
  "sqft": 1500,
  "bedrooms": 3,
  "bathrooms": 2,
  "latitude": 34.05,
  "longitude": -118.25,
  "median_income": 3.5,
  "house_age": 25,
  "population": 1500,
  "model_preference": "auto",
  "criteria": {"priority": "accuracy"}
}

# Compare all models
POST http://localhost:5000/predict/compare
```

## Troubleshooting

### Backend Won't Start

**Issue**: `ModuleNotFoundError` when starting backend

**Solution**:
```bash
# Make sure virtual environment is activated
cd backend
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Won't Start

**Issue**: `Cannot find module` error

**Solution**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Model Training Fails

**Issue**: `CUDA out of memory` or similar

**Solution**:
- Reduce batch size in training
- Use CPU instead of GPU
- Close other applications

**Issue**: `FileNotFoundError` when loading model

**Solution**:
- Train the model first using `python train.py [model_type]`
- Check that `backend/data/` directory exists
- Ensure model files were saved correctly

### Prediction Returns Error

**Issue**: `Model not found`

**Solution**:
- Train at least one model before making predictions
- Check model files exist in `backend/data/`

**Issue**: `Failed to connect to server`

**Solution**:
- Ensure backend is running on port 5000
- Check firewall settings
- Try accessing `http://localhost:5000/health`

### Dependencies Issues

**Issue**: PyTorch installation fails

**Solution**:
```bash
# Install PyTorch separately based on your system
# For CPU only:
pip install torch --index-url https://download.pytorch.org/whl/cpu

# For CUDA 11.8:
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

**Issue**: LangGraph import error

**Solution**:
```bash
pip install --upgrade langgraph langchain-core
```

## Project Structure

```
ai-deep-learning-example/
├── backend/
│   ├── models/                   # Model implementations
│   │   ├── base_model.py        # Abstract base class
│   │   ├── tensorflow_model.py  # TensorFlow implementation
│   │   ├── pytorch_model.py     # PyTorch implementation
│   │   └── huggingface_model.py # Transformer implementation
│   ├── router/                   # LangGraph routing
│   │   ├── langgraph_router.py  # Decision graph
│   │   └── model_selector.py    # Selection logic
│   ├── data/                     # Saved models (created on first train)
│   ├── api.py                    # FastAPI server
│   ├── train.py                  # Training script
│   └── requirements.txt          # Python dependencies
├── frontend/
│   ├── app/                      # Next.js app
│   ├── components/               # React components
│   │   ├── PredictionForm.tsx   # Prediction interface
│   │   ├── TrainingPanel.tsx    # Training interface
│   │   └── ModelComparison.tsx  # Model comparison view
│   └── package.json              # Node dependencies
├── MODEL_COMPARISON.md           # Detailed model comparison
├── SETUP_GUIDE.md               # This file
└── README.md                     # Project overview
```

## Testing the System

### 1. Test Backend Health

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Multi-model API is running",
  "available_models": ["tensorflow", "pytorch", "huggingface", "ensemble"]
}
```

### 2. Train a Model

```bash
# Train TensorFlow model
python backend/train.py tensorflow
```

This should:
- Load California housing dataset (20,640 samples)
- Train for 500 epochs
- Display progress every 100 epochs
- Show final metrics (R², RMSE)
- Save model to `backend/data/`

### 3. Make a Test Prediction

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sqft": 2000,
    "bedrooms": 4,
    "bathrooms": 2,
    "latitude": 37.77,
    "longitude": -122.42,
    "model_preference": "tensorflow"
  }'
```

Expected response includes:
- `predicted_price`: numerical value
- `model_used`: "tensorflow"
- `routing_explanation`: explanation text

### 4. Test All Models

```bash
# Train all
python backend/train.py all

# Compare predictions
curl -X POST http://localhost:5000/predict/compare \
  -H "Content-Type: application/json" \
  -d '{
    "sqft": 1500,
    "bedrooms": 3,
    "bathrooms": 2,
    "latitude": 34.05,
    "longitude": -118.25
  }'
```

## Performance Benchmarks

Expected training times (on CPU):
- **TensorFlow**: ~75 seconds (500 epochs)
- **PyTorch**: ~60 seconds (500 epochs)
- **Transformer**: ~125 seconds (500 epochs)
- **All three**: ~260 seconds

Expected accuracy (Test R²):
- **TensorFlow**: ~0.80
- **PyTorch**: ~0.80
- **Transformer**: ~0.79
- **Ensemble**: ~0.81

## Next Steps

1. **Train all models**: `python backend/train.py all`
2. **Explore the UI**: Open `http://localhost:3000`
3. **Try different selections**: Test Auto mode with different priorities
4. **Compare models**: Use the comparison view to see differences
5. **Read documentation**: Check `MODEL_COMPARISON.md` for deep dive

## Support

For issues or questions:
1. Check this guide's Troubleshooting section
2. Review `MODEL_COMPARISON.md` for model details
3. Check API documentation at `http://localhost:5000/docs`
4. Review code comments in source files

## Advanced Configuration

### Custom Training Parameters

```python
# In train.py, you can modify:
model.train_model(
    epochs=1000,           # More epochs for better accuracy
    learning_rate=0.0001,  # Lower LR for fine-tuning
    hidden_sizes=[128, 64, 32]  # Larger network
)
```

### GPU Acceleration

```bash
# Check if PyTorch detects GPU
python -c "import torch; print(torch.cuda.is_available())"

# Check if TensorFlow detects GPU
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

### Custom Routing Logic

Edit `backend/router/model_selector.py` to customize model selection logic based on your needs.

---

**Congratulations!** You now have a fully functional multi-model neural network system with intelligent routing. Explore, experiment, and learn! 🚀

