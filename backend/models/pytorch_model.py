"""
PyTorch Neural Network implementation for house price prediction
Identical architecture to TensorFlow version for fair comparison
"""
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import pickle
from typing import List
from .base_model import BaseHousingModel


class PyTorchNN(nn.Module):
    """
    PyTorch Neural Network with same architecture as TensorFlow model
    Architecture: input → 64 → 32 → 16 → output
    """
    
    def __init__(self, input_size=8, hidden_sizes=[64, 32, 16], output_size=1):
        super(PyTorchNN, self).__init__()
        
        layers = []
        prev_size = input_size
        
        # Build hidden layers with ReLU activation
        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(nn.ReLU())
            prev_size = hidden_size
        
        # Output layer (no activation for regression)
        layers.append(nn.Linear(prev_size, output_size))
        
        self.network = nn.Sequential(*layers)
        
        # Initialize weights using He initialization (similar to TensorFlow)
        self._initialize_weights()
    
    def _initialize_weights(self):
        """Initialize weights using He initialization for ReLU"""
        for module in self.network.modules():
            if isinstance(module, nn.Linear):
                nn.init.kaiming_normal_(module.weight, mode='fan_in', nonlinearity='relu')
                if module.bias is not None:
                    nn.init.constant_(module.bias, 0)
    
    def forward(self, x):
        return self.network(x)


class PyTorchModel(BaseHousingModel):
    """
    PyTorch implementation of house price prediction model
    Implements BaseHousingModel interface
    """
    
    def __init__(self, input_size=8, hidden_sizes=[64, 32, 16], output_size=1, learning_rate=0.001):
        """
        Initialize PyTorch neural network
        
        Args:
            input_size: Number of input features
            hidden_sizes: List of hidden layer sizes
            output_size: Number of output neurons
            learning_rate: Learning rate for Adam optimizer
        """
        super().__init__(input_size, hidden_sizes, output_size, learning_rate)
        
        # Set device (GPU if available, else CPU)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Initialize model
        self.model = PyTorchNN(input_size, hidden_sizes, output_size).to(self.device)
        
        # Initialize optimizer
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        
        # Loss function (MSE for regression)
        self.criterion = nn.MSELoss()
    
    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 500, 
              batch_size: int = 32, verbose: bool = True) -> List[float]:
        """
        Train the PyTorch model
        
        Args:
            X: Training features
            y: Training labels
            epochs: Number of training epochs
            batch_size: Batch size for training
            verbose: Print training progress
            
        Returns:
            List of losses per epoch
        """
        # Convert numpy arrays to PyTorch tensors
        X_tensor = torch.FloatTensor(X).to(self.device)
        y_tensor = torch.FloatTensor(y).to(self.device)
        
        # Create dataset and dataloader
        dataset = TensorDataset(X_tensor, y_tensor)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        # Training loop
        losses = []
        self.model.train()
        
        for epoch in range(epochs):
            epoch_loss = 0.0
            batch_count = 0
            
            for batch_X, batch_y in dataloader:
                # Forward pass
                predictions = self.model(batch_X)
                loss = self.criterion(predictions, batch_y)
                
                # Backward pass and optimization
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                
                epoch_loss += loss.item()
                batch_count += 1
            
            # Average loss for epoch
            avg_loss = epoch_loss / batch_count
            losses.append(avg_loss)
            
            # Print progress
            if verbose and (epoch + 1) % 100 == 0:
                print(f"Epoch {epoch + 1}, Loss: {avg_loss:.4f}")
        
        return losses
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions
        
        Args:
            X: Input features
            
        Returns:
            Predictions as numpy array
        """
        self.model.eval()
        
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).to(self.device)
            predictions = self.model(X_tensor)
            return predictions.cpu().numpy()
    
    def save(self, filepath: str) -> None:
        """
        Save PyTorch model to disk
        
        Args:
            filepath: Path to save the model
        """
        if filepath.endswith('.pkl'):
            filepath = filepath[:-4]
        
        # Save model state dict
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
        }, f"{filepath}.pt")
        
        # Save metadata
        metadata = {
            'input_size': self.input_size,
            'hidden_sizes': self.hidden_sizes,
            'output_size': self.output_size,
            'learning_rate': self.learning_rate,
            'model_type': 'pytorch'
        }
        with open(f"{filepath}_metadata.pkl", 'wb') as f:
            pickle.dump(metadata, f)
    
    def load(self, filepath: str) -> None:
        """
        Load PyTorch model from disk
        
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
        
        # Rebuild model with loaded architecture
        self.model = PyTorchNN(self.input_size, self.hidden_sizes, self.output_size).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        
        # Load model weights
        checkpoint = torch.load(f"{filepath}.pt", map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        
        self.model.eval()
    
    def summary(self) -> None:
        """Print model architecture summary"""
        print("\n" + "="*70)
        print("PyTorch Model Architecture")
        print("="*70)
        print(self.model)
        print("="*70)
        
        # Count parameters
        total_params = sum(p.numel() for p in self.model.parameters())
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        
        print(f"\nTotal parameters: {total_params:,}")
        print(f"Trainable parameters: {trainable_params:,}")
        print(f"Device: {self.device}")
        print("="*70 + "\n")
    
    def get_param_count(self) -> int:
        """Get total number of trainable parameters"""
        return sum(p.numel() for p in self.model.parameters() if p.requires_grad)

