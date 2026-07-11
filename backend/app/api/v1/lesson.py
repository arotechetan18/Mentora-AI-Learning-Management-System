from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.database import get_db
from ...core.security import get_current_user
from ...models.user import User
from ...models.lesson import Lesson
from ...models.quiz_question import QuizQuestion
from ...models.lesson_progress import LessonProgress
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(tags=["Lessons"])

# ==================== SCHEMAS ====================
class QuizQuestionResponse(BaseModel):
    id: int
    question: str
    options: List[str]
    explanation: Optional[str]

class LessonContentResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    concept: Optional[str]
    example: Optional[str]
    interview_questions: Optional[str]
    duration: int
    order: int
    is_completed: bool = False
    quiz: List[QuizQuestionResponse] = []
    next_lesson_id: Optional[int]
    prev_lesson_id: Optional[int]

class QuizSubmit(BaseModel):
    answers: List[int]

class QuizResultResponse(BaseModel):
    score: int
    total: int
    percentage: float
    passed: bool
    results: List[dict]

# ==================== GET LESSON CONTENT ====================
@router.get("/lessons/{lesson_id}", response_model=LessonContentResponse)
def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    progress = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.lesson_id == lesson_id
    ).first()
    
    prev = db.query(Lesson).filter(
        Lesson.module_id == lesson.module_id,
        Lesson.order < lesson.order
    ).order_by(Lesson.order.desc()).first()
    
    next = db.query(Lesson).filter(
        Lesson.module_id == lesson.module_id,
        Lesson.order > lesson.order
    ).order_by(Lesson.order.asc()).first()
    
    quiz = db.query(QuizQuestion).filter(QuizQuestion.lesson_id == lesson_id).all()
    
    return {
        "id": lesson.id,
        "title": lesson.title,
        "description": lesson.description,
        "concept": lesson.concept,
        "example": lesson.example,
        "interview_questions": lesson.interview_questions,
        "duration": lesson.duration,
        "order": lesson.order,
        "is_completed": progress.is_completed if progress else False,
        "quiz": quiz,
        "next_lesson_id": next.id if next else None,
        "prev_lesson_id": prev.id if prev else None
    }

# ==================== SUBMIT QUIZ ====================
@router.post("/lessons/{lesson_id}/quiz", response_model=QuizResultResponse)
def submit_quiz(
    lesson_id: int,
    quiz_data: QuizSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    questions = db.query(QuizQuestion).filter(QuizQuestion.lesson_id == lesson_id).all()
    
    if len(quiz_data.answers) != len(questions):
        raise HTTPException(status_code=400, detail="Please answer all questions")
    
    correct = 0
    results = []
    
    for i, q in enumerate(questions):
        is_correct = quiz_data.answers[i] == q.correct_answer
        if is_correct:
            correct += 1
        results.append({
            "question_id": q.id,
            "selected": quiz_data.answers[i],
            "correct": q.correct_answer,
            "is_correct": is_correct,
            "explanation": q.explanation
        })
    
    total = len(questions)
    percentage = (correct / total) * 100
    passed = percentage >= 60
    
    return {
        "score": correct,
        "total": total,
        "percentage": round(percentage, 2),
        "passed": passed,
        "results": results
    }

# ==================== UPDATE PROGRESS ====================
@router.put("/lessons/{lesson_id}/progress")
def update_progress(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    progress = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.lesson_id == lesson_id
    ).first()
    
    if not progress:
        progress = LessonProgress(
            user_id=current_user.id,
            lesson_id=lesson_id
        )
        db.add(progress)
    
    progress.is_completed = True
    progress.completed_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Progress updated", "completed": True}