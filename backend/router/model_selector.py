"""
Model Selection Logic

Contains criteria and logic for selecting the appropriate model
based on request parameters and preferences.
"""
from typing import Dict, Optional, Literal

ModelType = Literal['tensorflow', 'pytorch', 'huggingface', 'ensemble']


def select_model_by_criteria(
    model_preference: Optional[str] = "auto",
    criteria: Optional[Dict] = None
) -> ModelType:
    """
    Select model based on preference and criteria
    
    Args:
        model_preference: Explicit model choice or "auto"
        criteria: Dictionary with selection criteria
            - priority: "speed", "accuracy", "experimental", "balanced"
            - dataset_size: "small", "medium", "large"
            - use_case: "production", "research", "demo"
    
    Returns:
        Selected model type
    """
    # If explicit preference provided, use it
    if model_preference and model_preference != "auto":
        if model_preference in ['tensorflow', 'pytorch', 'huggingface', 'ensemble']:
            return model_preference
    
    # Default criteria
    if criteria is None:
        criteria = {"priority": "accuracy"}
    
    priority = criteria.get("priority", "accuracy")
    dataset_size = criteria.get("dataset_size", "medium")
    use_case = criteria.get("use_case", "production")
    
    # Selection logic based on criteria
    
    # Priority-based selection
    if priority == "speed":
        # PyTorch typically has fastest inference
        return "pytorch"
    
    elif priority == "accuracy":
        # TensorFlow (well-optimized, proven)
        return "tensorflow"
    
    elif priority == "experimental":
        # Transformer architecture for learning
        return "huggingface"
    
    elif priority == "balanced":
        # Ensemble for best overall results
        return "ensemble"
    
    # Use case based selection
    elif use_case == "production":
        return "tensorflow"  # Most stable
    
    elif use_case == "research":
        return "huggingface"  # Most interesting
    
    elif use_case == "demo":
        return "pytorch"  # Fast and lightweight
    
    # Default fallback
    return "tensorflow"


def get_model_characteristics() -> Dict[str, Dict]:
    """
    Get characteristics of each model for comparison
    
    Returns:
        Dictionary with model characteristics
    """
    return {
        "tensorflow": {
            "name": "TensorFlow/Keras ANN",
            "architecture": "Dense Feedforward Network",
            "layers": "8 → 64 → 32 → 16 → 1",
            "parameters": "~3,201",
            "framework": "TensorFlow 2.17",
            "activation": "ReLU (hidden), Linear (output)",
            "optimizer": "Adam",
            "strengths": [
                "Industry standard",
                "Excellent documentation",
                "Production-ready",
                "Well-optimized",
                "GPU acceleration"
            ],
            "best_for": "Production deployments, proven results",
            "training_speed": "Medium",
            "inference_speed": "Fast",
            "typical_use": "General ML tasks, CV, production systems"
        },
        "pytorch": {
            "name": "PyTorch ANN",
            "architecture": "Dense Feedforward Network",
            "layers": "8 → 64 → 32 → 16 → 1",
            "parameters": "~3,201",
            "framework": "PyTorch 2.1",
            "activation": "ReLU (hidden), Linear (output)",
            "optimizer": "Adam",
            "strengths": [
                "Research-friendly",
                "Pythonic API",
                "Dynamic computation graph",
                "Fastest inference",
                "Great debugging"
            ],
            "best_for": "Research, experimentation, custom architectures",
            "training_speed": "Fast",
            "inference_speed": "Very Fast",
            "typical_use": "Research, custom models, rapid prototyping"
        },
        "huggingface": {
            "name": "Transformer Model",
            "architecture": "Transformer Encoder (adapted for tabular)",
            "layers": "Projection → 2x Transformer Layers → Dense",
            "parameters": "~15,000+",
            "framework": "PyTorch + Transformers",
            "activation": "Self-Attention + ReLU",
            "optimizer": "Adam",
            "strengths": [
                "Attention mechanism",
                "Captures complex patterns",
                "State-of-art for NLP",
                "Transfer learning potential",
                "Educational value"
            ],
            "best_for": "Learning transformers, experimental approaches",
            "training_speed": "Slower",
            "inference_speed": "Medium",
            "typical_use": "NLP, vision transformers, complex sequences"
        },
        "ensemble": {
            "name": "Ensemble (All 3 Models)",
            "architecture": "Combines TensorFlow, PyTorch, and Transformer",
            "layers": "Average of all model predictions",
            "parameters": "Sum of all models",
            "framework": "Multi-framework",
            "activation": "Various",
            "optimizer": "Various",
            "strengths": [
                "Best accuracy",
                "Reduces variance",
                "Robust predictions",
                "Combines strengths",
                "Production-grade results"
            ],
            "best_for": "Maximum accuracy, critical predictions",
            "training_speed": "N/A (uses trained models)",
            "inference_speed": "Slow (3x)",
            "typical_use": "Competitions, critical applications"
        }
    }


def explain_selection(model_type: str, criteria: Optional[Dict] = None) -> str:
    """
    Explain why a particular model was selected
    
    Args:
        model_type: Selected model type
        criteria: Criteria used for selection
    
    Returns:
        Human-readable explanation
    """
    characteristics = get_model_characteristics()
    model_info = characteristics.get(model_type, {})
    
    explanation = f"Selected {model_info.get('name', model_type)} because:\n"
    
    if criteria:
        priority = criteria.get("priority", "balanced")
        explanation += f"- Priority: {priority}\n"
        explanation += f"- Best for: {model_info.get('best_for', 'general use')}\n"
    
    explanation += f"- Architecture: {model_info.get('architecture', 'N/A')}\n"
    explanation += f"- Training speed: {model_info.get('training_speed', 'N/A')}\n"
    explanation += f"- Inference speed: {model_info.get('inference_speed', 'N/A')}\n"
    
    return explanation

