from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class LessonBase(BaseModel):
    title: str
    description: Optional[str] = None
    concept: Optional[str] = Field(default=None, description="Theory concept")
    example: Optional[str] = Field(default=None, description="Real-life + Code example")
    interview_questions: Optional[str] = Field(default=None, description="Interview questions")
    duration: int = Field(default=0, description="Duration in minutes")
    order: int = Field(default=0, description="Lesson order in module")

class LessonCreate(LessonBase):
    module_id: int

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    concept: Optional[str] = None
    example: Optional[str] = None
    interview_questions: Optional[str] = None
    duration: Optional[int] = None
    order: Optional[int] = None

class LessonResponse(LessonBase):
    id: int
    module_id: int
    course_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_completed: bool = Field(default=False, description="Is lesson completed by user")
    is_locked: bool = Field(default=False, description="Is lesson locked")
    
    class Config:
        from_attributes = True