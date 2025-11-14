"""Model information schemas"""
from pydantic import BaseModel
from typing import Dict


class ModelInfoResponse(BaseModel):
    success: bool
    models: Dict[str, dict]
    message: str

