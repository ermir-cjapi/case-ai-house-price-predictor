"""Training-related schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List


class TrainRequest(BaseModel):
    epochs: Optional[int] = Field(default=500, description="Number of training epochs")
    learning_rate: Optional[float] = Field(default=0.001, description="Learning rate for training")
    hidden_sizes: Optional[List[int]] = Field(default=[64, 32, 16], description="Hidden layer sizes")


class TrainResponse(BaseModel):
    success: bool
    message: str
    model_type: str
    metrics: Optional[dict] = None


class AsyncTrainResponse(BaseModel):
    success: bool
    task_id: str
    message: str
    model_type: str

