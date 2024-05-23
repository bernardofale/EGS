from pydantic import BaseModel
from datetime import datetime


# Defining Pydantic models
class ToDoItemCreate(BaseModel):
    description: str
    completed: bool = False
    priority: int = 1
    meeting_id: str
    content: str
    departamento_id: int
    due_date: datetime
