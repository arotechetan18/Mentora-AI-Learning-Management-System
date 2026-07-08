from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EnrollmentCreate(BaseModel):
    course_id: int

class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime
    progress: float
    completed: bool
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True