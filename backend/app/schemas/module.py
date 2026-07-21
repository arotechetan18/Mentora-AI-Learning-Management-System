from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class ModuleBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: int = Field(default=0, description="Module order in course")

class ModuleCreate(ModuleBase):
    course_id: int

class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None

class ModuleResponse(ModuleBase):
    id: int
    course_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    lessons: Optional[List['LessonResponse']] = []
    
    class Config:
        from_attributes = True

# Circular import साठी forward reference
from .lesson import LessonResponse
ModuleResponse.model_rebuild()