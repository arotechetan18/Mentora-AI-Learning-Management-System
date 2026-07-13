from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProgressUpdate(BaseModel):
    current_lesson: Optional[str] = None
    study_time: Optional[int] = None

class ProgressResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    current_lesson: Optional[str]
    completion_percentage: float
    study_time: int
    last_studied: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

class DashboardResponse(BaseModel):
    total_courses: int
    completed_courses: int
    in_progress_courses: int
    total_quizzes_taken: int
    average_quiz_score: float
    total_study_time: int
    certificates_earned: int
    overall_progress: float

class CourseProgressResponse(BaseModel):
    course_id: int
    total_lessons: int
    completed_lessons: int
    progress: float
    is_completed: bool