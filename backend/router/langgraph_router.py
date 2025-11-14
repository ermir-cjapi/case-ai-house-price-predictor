"""
LangGraph Router for Intelligent Model Selection

Uses LangGraph to create a decision graph that routes requests
to the appropriate model based on criteria and context.
"""
from typing import Dict, List, Optional, TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, END
from .model_selector import select_model_by_criteria, get_model_characteristics


class ModelState(TypedDict):
    """State for the model selection graph"""
    features: Dict  # Input features for prediction
    model_preference: Optional[str]  # User's model preference
    criteria: Optional[Dict]  # Selection criteria
    selected_model: Optional[str]  # Selected model type
    predictions: Dict[str, float]  # Predictions from each model
    final_prediction: Optional[float]  # Final prediction result
    explanation: str  # Explanation of model selection
    ensemble_weights: Dict[str, float]  # Weights for ensemble
    metadata: Dict  # Additional metadata


def analyze_request(state: ModelState) -> ModelState:
    """
    Analyze the incoming request and extract criteria
    
    This node examines the request and determines what criteria
    should be used for model selection.
    """
    # Extract criteria from state
    criteria = state.get("criteria", {})
    model_preference = state.get("model_preference", "auto")
    
    # Add default criteria if not provided
    if not criteria:
        criteria = {"priority": "accuracy"}
    
    # Analyze features to provide context
    features = state.get("features", {})
    
    # Add metadata about the request
    metadata = {
        "feature_count": len(features),
        "has_preference": model_preference != "auto",
        "analysis_complete": True
    }
    
    state["criteria"] = criteria
    state["metadata"] = metadata
    state["explanation"] = "Request analyzed and ready for routing."
    
    return state


def route_to_model(state: ModelState) -> str:
    """
    Routing function that decides which model to use
    
    This is the conditional edge function that determines
    the next node based on the selected model.
    """
    # Use model selector to choose model
    model_preference = state.get("model_preference", "auto")
    criteria = state.get("criteria", {})
    
    selected_model = select_model_by_criteria(model_preference, criteria)
    
    # Store selection in state
    state["selected_model"] = selected_model
    
    # Return the routing decision
    if selected_model == "ensemble":
        return "ensemble"
    else:
        return selected_model


def use_tensorflow_model(state: ModelState) -> ModelState:
    """Node for TensorFlow model prediction"""
    state["selected_model"] = "tensorflow"
    state["explanation"] = "Using TensorFlow model: Industry standard, production-ready"
    
    # Actual prediction will be done by the caller
    # This node just marks the selection
    return state


def use_pytorch_model(state: ModelState) -> ModelState:
    """Node for PyTorch model prediction"""
    state["selected_model"] = "pytorch"
    state["explanation"] = "Using PyTorch model: Fast inference, research-friendly"
    
    return state


def use_huggingface_model(state: ModelState) -> ModelState:
    """Node for Hugging Face transformer prediction"""
    state["selected_model"] = "huggingface"
    state["explanation"] = "Using Transformer model: Advanced architecture with attention mechanism"
    
    return state


def ensemble_predictions(state: ModelState) -> ModelState:
    """
    Node for ensemble prediction
    
    This would combine predictions from all three models.
    Actual ensemble logic is handled by the caller.
    """
    state["selected_model"] = "ensemble"
    state["explanation"] = "Using Ensemble: Combining all three models for maximum accuracy"
    
    # Default ensemble weights (can be adjusted based on validation performance)
    state["ensemble_weights"] = {
        "tensorflow": 0.4,
        "pytorch": 0.3,
        "huggingface": 0.3
    }
    
    return state


class ModelRouter:
    """
    LangGraph-based router for model selection
    
    This class encapsulates the decision graph for routing
    requests to the appropriate model.
    """
    
    def __init__(self):
        """Initialize the router with compiled graph"""
        self.graph = self._create_graph()
        self.characteristics = get_model_characteristics()
    
    def _create_graph(self) -> StateGraph:
        """
        Create and compile the LangGraph decision graph
        
        Returns:
            Compiled StateGraph
        """
        # Create the graph
        workflow = StateGraph(ModelState)
        
        # Add nodes
        workflow.add_node("analyze", analyze_request)
        workflow.add_node("select_tensorflow", use_tensorflow_model)
        workflow.add_node("select_pytorch", use_pytorch_model)
        workflow.add_node("select_huggingface", use_huggingface_model)
        workflow.add_node("ensemble", ensemble_predictions)
        
        # Set entry point
        workflow.set_entry_point("analyze")
        
        # Add conditional edges from analyze node
        workflow.add_conditional_edges(
            "analyze",
            route_to_model,
            {
                "tensorflow": "select_tensorflow",
                "pytorch": "select_pytorch",
                "huggingface": "select_huggingface",
                "ensemble": "ensemble"
            }
        )
        
        # All model selection nodes go to END
        workflow.add_edge("select_tensorflow", END)
        workflow.add_edge("select_pytorch", END)
        workflow.add_edge("select_huggingface", END)
        workflow.add_edge("ensemble", END)
        
        return workflow.compile()
    
    def route(self, features: Dict, model_preference: str = "auto", 
              criteria: Optional[Dict] = None) -> Dict:
        """
        Route a prediction request to the appropriate model
        
        Args:
            features: Input features for prediction
            model_preference: User's model preference
            criteria: Selection criteria
        
        Returns:
            Dictionary with routing decision and metadata
        """
        # Create initial state
        initial_state: ModelState = {
            "features": features,
            "model_preference": model_preference,
            "criteria": criteria or {},
            "selected_model": None,
            "predictions": {},
            "final_prediction": None,
            "explanation": "",
            "ensemble_weights": {},
            "metadata": {}
        }
        
        # Run the graph
        result = self.graph.invoke(initial_state)
        
        return {
            "selected_model": result["selected_model"],
            "explanation": result["explanation"],
            "ensemble_weights": result.get("ensemble_weights", {}),
            "metadata": result.get("metadata", {}),
            "model_info": self.characteristics.get(result["selected_model"], {})
        }
    
    def get_model_info(self, model_type: str) -> Dict:
        """Get information about a specific model"""
        return self.characteristics.get(model_type, {})
    
    def get_all_models_info(self) -> Dict[str, Dict]:
        """Get information about all available models"""
        return self.characteristics


def create_model_router() -> ModelRouter:
    """
    Factory function to create a ModelRouter instance
    
    Returns:
        Configured ModelRouter
    """
    return ModelRouter()

