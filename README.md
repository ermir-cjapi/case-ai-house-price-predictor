# House Price Predictor with TensorFlow

An AI-powered house price prediction application built with TensorFlow/Keras. The project features a Python backend with a professional neural network implementation and a modern Next.js frontend.

> **📝 Note:** The codebase has been recently restructured for better organization and maintainability. See `docs/RESTRUCTURE_COMPLETE.md` for details.

## Features

- **Neural Network with TensorFlow**: Professional implementation using Keras
  - 3 hidden layers (64 → 32 → 16 neurons)
  - ReLU activation functions
  - Adam optimizer (adaptive learning rate)
  - He weight initialization
  - Mean Squared Error (MSE) loss function

- **California Housing Dataset**: Real-world data with ~20,000 samples
  - 8 input features including location, house characteristics, and demographics
  - Trained to predict house prices in hundreds of thousands of dollars

- **Full-Stack Application**:
  - Python FastAPI backend with REST API
  - Next.js 14 frontend with TypeScript
  - Modern, responsive UI with Tailwind CSS
  - Real-time model training and prediction

## Project Structure

```
ai-deep-learning-example/
├── backend/
│   ├── ann.py              # Neural Network with TensorFlow/Keras
│   ├── train.py            # Training script
│   ├── api.py              # FastAPI server
│   ├── requirements.txt    # Python dependencies
│   └── data/               # Model storage (created on first run)
├── frontend/
│   ├── app/
│   │   ├── page.tsx        # Main UI page
│   │   ├── layout.tsx      # App layout
│   │   ├── globals.css     # Global styles
│   │   └── api/            # Next.js API routes
│   ├── components/
│   │   ├── PredictionForm.tsx    # Prediction input form
│   │   └── TrainingPanel.tsx     # Training control panel
│   ├── package.json
│   └── next.config.js
└── README.md
```

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- npm or yarn

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

## Running the Application

### Start the Backend Server

1. From the `backend` directory:
```bash
python api.py
```

The FastAPI server will start on `http://localhost:5000`

### Start the Frontend Development Server

1. From the `frontend` directory:
```bash
npm run dev
```

The Next.js app will start on `http://localhost:3000`

2. Open your browser and navigate to `http://localhost:3000`

## Usage

### Training the Model

1. Click the "Train Model" button in the Training Panel
2. Configure the number of epochs (default: 500)
3. Wait for training to complete (may take a few minutes)
4. View training metrics including R² score and RMSE

### Making Predictions

1. Enter house features in the Prediction Form:
   - Square Footage
   - Number of Bedrooms
   - Number of Bathrooms
   - House Age
   - Median Income in the area
   - Location (Latitude/Longitude)

2. Use the "Quick Select" buttons for popular California cities

3. Click "Predict Price" to get the estimated house price

## API Endpoints

### Backend API (FastAPI)

- `GET /health` - Health check
- `GET /model-info` - Get model information and training status
- `POST /train` - Train the neural network
  - Body: `{ epochs: number, learning_rate: number, hidden_sizes: number[] }`
  - Returns: Training metrics
- `POST /predict` - Predict house price
  - Body: `{ sqft, bedrooms, bathrooms, latitude, longitude, median_income, house_age }`
  - Returns: Predicted price
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

### Frontend API (Next.js)

- `POST /api/train` - Proxy to backend training endpoint
- `POST /api/predict` - Proxy to backend prediction endpoint

## Model Architecture

The custom ANN consists of:

- **Input Layer**: 8 features
  - MedInc (Median Income)
  - HouseAge
  - AveRooms (Average Rooms)
  - AveBedrms (Average Bedrooms)
  - Population
  - AveOccup (Average Occupancy)
  - Latitude
  - Longitude

- **Hidden Layers**:
  - Layer 1: 64 neurons (ReLU)
  - Layer 2: 32 neurons (ReLU)
  - Layer 3: 16 neurons (ReLU)

- **Output Layer**: 1 neuron (Linear activation for regression)

## Training Details

- **Optimizer**: Mini-batch Gradient Descent
- **Batch Size**: 32
- **Learning Rate**: 0.001
- **Weight Initialization**: He initialization
- **Loss Function**: Mean Squared Error (MSE)
- **Dataset Split**: 80% training, 20% testing

## Technologies Used

### Backend
- Python 3.10+
- FastAPI 0.104.1 (Web framework)
- Uvicorn 0.24.0 (ASGI server)
- Pydantic 2.5.0 (Data validation)
- TensorFlow 2.15.0 (Neural network framework)
- NumPy 1.24.3 (Array operations)
- scikit-learn 1.3.0 (Dataset loading and preprocessing)

### Frontend
- Next.js 14 (React framework)
- TypeScript (Type safety)
- Tailwind CSS (Styling)
- Axios (HTTP client)

## Learning Objectives

This project demonstrates:

1. **Neural Network with TensorFlow**:
   - Building models with Keras Sequential API
   - Training with modern optimizers (Adam)
   - Model saving and loading
   - Activation functions and architecture design

2. **Machine Learning Pipeline**:
   - Data preprocessing and normalization
   - Train-test splitting
   - Model evaluation metrics
   - Model persistence

3. **Full-Stack Development**:
   - RESTful API design
   - React component architecture
   - State management
   - API integration

## Performance

Expected model performance:
- **R² Score**: ~0.75-0.85 (75-85% accuracy)
- **RMSE**: ~$40,000-$60,000
- **Training Time**: 1-3 minutes for 500 epochs

## Troubleshooting

### Backend Issues

- **Port 5000 already in use**: Change the port in `api.py`
- **Module not found**: Ensure virtual environment is activated and dependencies are installed
- **Dataset download fails**: Check internet connection (scikit-learn downloads the dataset)

### Frontend Issues

- **Cannot connect to backend**: Ensure FastAPI server is running on port 5000
- **Port 3000 already in use**: Use `npm run dev -- -p 3001` to use a different port

## Future Enhancements

- Add data visualization (loss curves, feature importance)
- Implement more advanced optimizers (Adam, RMSprop)
- Add regularization techniques (L2, dropout)
- Support for additional datasets
- Model comparison and A/B testing
- Real-time training progress updates with WebSockets

## License

This project is created for educational purposes.

## Author

Built as a learning project to understand neural networks and full-stack ML applications.

