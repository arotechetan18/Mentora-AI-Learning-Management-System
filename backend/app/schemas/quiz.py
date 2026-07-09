from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# ==================== QUESTION SCHEMAS ====================
class QuestionBase(BaseModel):
    question_text: str
    options: List[str]  # ["A", "B", "C", "D"]
    correct_answer: int  # Index of correct option
    explanation: Optional[str] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: int
    quiz_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ==================== QUIZ SCHEMAS ====================
class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    time_limit: Optional[int] = None  # minutes
    passing_score: float = 70.0
    is_published: bool = False

class QuizCreate(QuizBase):
    questions: List[QuestionCreate]  # At least 1 question

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    time_limit: Optional[int] = None
    passing_score: Optional[float] = None
    is_published: Optional[bool] = None

class QuizResponse(QuizBase):
    id: int
    course_id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime]
    questions: List[QuestionResponse] = []
    
    class Config:
        from_attributes = True

# ==================== QUIZ ATTEMPT SCHEMAS ====================
class QuizAttemptSubmit(BaseModel):
    answers: List[int]  # User's answers [0, 1, 2, 3]

class QuizAttemptResponse(BaseModel):
    id: int
    user_id: int
    quiz_id: int
    score: float
    answers: List[int]
    passed: bool
    attempted_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class QuizResultResponse(BaseModel):
    quiz_id: int
    quiz_title: str
    total_questions: int
    correct_answers: int
    score: float
    passed: bool
    passing_score: float
    attempt_id: int
    attempted_at: datetime