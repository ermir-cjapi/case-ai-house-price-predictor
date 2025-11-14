"""Task status schemas"""
from pydantic import BaseModel
from typing import Optional


class TaskStatusResponse(BaseModel):
    task_id: str
    state: str
    progress: Optional[dict] = None
    result: Optional[dict] = None
    error: Optional[str] = None

