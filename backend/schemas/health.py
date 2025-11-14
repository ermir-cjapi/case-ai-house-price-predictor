"""Health check schemas"""
from pydantic import BaseModel
from typing import List


class HealthResponse(BaseModel):
    status: str
    message: str
    available_models: List[str]

