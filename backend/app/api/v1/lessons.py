from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.database import get_db
from ...core.security import get_current_user
from ...models.user import User
from ...models.lesson import Lesson
from ...models.module import Module  # ✅ Module import
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
    
    # Get current module
    current_module = db.query(Module).filter(Module.id == lesson.module_id).first()
    
    # ✅ Get Previous Lesson (Same Module or Previous Module's Last Lesson)
    prev_lesson = db.query(Lesson).filter(
        Lesson.module_id == lesson.module_id,
        Lesson.order < lesson.order
    ).order_by(Lesson.order.desc()).first()
    
    if not prev_lesson:
        # Get previous module's last lesson
        prev_module = db.query(Module).filter(
            Module.course_id == current_module.course_id,
            Module.order < current_module.order
        ).order_by(Module.order.desc()).first()
        if prev_module:
            prev_lesson = db.query(Lesson).filter(
                Lesson.module_id == prev_module.id
            ).order_by(Lesson.order.desc()).first()
    
    # ✅ Get Next Lesson (Same Module or Next Module's First Lesson)
    next_lesson = db.query(Lesson).filter(
        Lesson.module_id == lesson.module_id,
        Lesson.order > lesson.order
    ).order_by(Lesson.order.asc()).first()
    
    if not next_lesson:
        # Get next module's first lesson
        next_module = db.query(Module).filter(
            Module.course_id == current_module.course_id,
            Module.order > current_module.order
        ).order_by(Module.order.asc()).first()
        if next_module:
            next_lesson = db.query(Lesson).filter(
                Lesson.module_id == next_module.id
            ).order_by(Lesson.order.asc()).first()
    
    # Get progress and quiz
    progress = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.lesson_id == lesson_id
    ).first()
    
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
        "next_lesson_id": next_lesson.id if next_lesson else None,
        "prev_lesson_id": prev_lesson.id if prev_lesson else None,
         "course_id": current_module.course_id
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