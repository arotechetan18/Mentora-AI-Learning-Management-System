from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...core.security import get_current_user
from ...models.user import User
from ...models.module import Module
from ...models.lesson import Lesson
from ...models.lesson_progress import LessonProgress
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(tags=["Modules"])

# ==================== SCHEMAS ====================
class LessonResponse(BaseModel):
    id: int
    title: str
    description: str | None
    concept: str | None
    example: str | None
    interview_questions: str | None
    duration: int
    order: int
    is_completed: bool = False
    created_at: datetime
    updated_at: datetime | None

class ModuleWithLessonsResponse(BaseModel):  # ✅ हा class define करा
    id: int
    course_id: int
    title: str
    description: str | None
    order: int
    lessons: List[LessonResponse] = []
    created_at: datetime
    updated_at: datetime | None

# ==================== API ====================
@router.get("/courses/{course_id}/modules", response_model=List[ModuleWithLessonsResponse])
def get_course_modules(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    modules = db.query(Module).filter(Module.course_id == course_id).order_by(Module.order).all()
    
    result = []
    for module in modules:
        lessons = db.query(Lesson).filter(Lesson.module_id == module.id).order_by(Lesson.order).all()
        
        lesson_responses = []
        for lesson in lessons:
            progress = db.query(LessonProgress).filter(
                LessonProgress.user_id == current_user.id,
                LessonProgress.lesson_id == lesson.id
            ).first()
            
            lesson_responses.append(LessonResponse(
                id=lesson.id,
                title=lesson.title,
                description=lesson.description,
                concept=lesson.concept,
                example=lesson.example,
                interview_questions=lesson.interview_questions,
                duration=lesson.duration,
                order=lesson.order,
                is_completed=progress.is_completed if progress else False,
                created_at=lesson.created_at,
                updated_at=lesson.updated_at
            ))
        
        result.append(ModuleWithLessonsResponse(
            id=module.id,
            course_id=module.course_id,
            title=module.title,
            description=module.description,
            order=module.order,
            lessons=lesson_responses,
            created_at=module.created_at,
            updated_at=module.updated_at
        ))
    
    return result