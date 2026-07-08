from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class CourseBase(BaseModel):
    title: str
    description: str
    category: str
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    duration: int
    price: float = 0.0

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None
    duration: Optional[int] = None
    price: Optional[float] = None
    is_published: Optional[bool] = None

class CourseResponse(CourseBase):
    id: int
    instructor_id: int
    is_published: bool
    cover_image: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True