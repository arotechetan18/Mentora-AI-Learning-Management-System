from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...core.security import get_current_user
from ...models.user import User
from ...models.course import Course
from ...models.enrollment import Enrollment
from ...models.progress import Progress
from ...models.lesson import Lesson
from ...models.lesson_progress import LessonProgress
from ...models.module import Module  # ✅ ADD THIS
from ...schemas.progress import ProgressResponse, DashboardResponse
from datetime import datetime

router = APIRouter(tags=["Progress"])

# ==================== GET DASHBOARD ====================
@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get all enrollments
    enrollments = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id
    ).all()
    
    total_courses = len(enrollments)
    completed_courses = sum(1 for e in enrollments if e.completed)
    in_progress_courses = sum(1 for e in enrollments if not e.completed and e.progress > 0)
    
    # Get total study time
    progress_records = db.query(Progress).filter(
        Progress.user_id == current_user.id
    ).all()
    total_study_time = sum(p.study_time for p in progress_records)
    
    # ✅ Calculate exact progress for each enrollment
    for enrollment in enrollments:
        # Get all lessons for this course
        total_lessons = db.query(Lesson).join(Lesson.module).filter(
            Lesson.module.has(course_id=enrollment.course_id)
        ).count()
        
        if total_lessons > 0:
            # Get completed lessons for this user and course
            completed_lessons = db.query(LessonProgress).join(
                LessonProgress.lesson
            ).join(
                Lesson.module
            ).filter(
                LessonProgress.user_id == current_user.id,
                LessonProgress.is_completed == True,
                Lesson.module.has(course_id=enrollment.course_id)
            ).count()
            
            # ✅ Exact progress calculation
            exact_progress = (completed_lessons / total_lessons) * 100
            enrollment.progress = round(exact_progress, 2)
            
            # Update completed status
            if exact_progress >= 100:
                enrollment.completed = True
                enrollment.completed_at = datetime.utcnow()
    
    db.commit()
    
    # Calculate overall progress
    overall_progress = sum(e.progress for e in enrollments) / len(enrollments) if enrollments else 0
    
    return DashboardResponse(
        total_courses=total_courses,
        completed_courses=completed_courses,
        in_progress_courses=in_progress_courses,
        total_quizzes_taken=0,
        average_quiz_score=0,
        total_study_time=total_study_time,
        certificates_earned=0,
        overall_progress=round(overall_progress, 2)
    )

# ==================== GET COURSE PROGRESS ====================
@router.get("/courses/{course_id}/progress")
def get_course_progress(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check enrollment
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Not enrolled in this course")
    
    # ✅ Get exact progress
    total_lessons = db.query(Lesson).join(Lesson.module).filter(
        Lesson.module.has(course_id=course_id)
    ).count()
    
    completed_lessons = 0
    if total_lessons > 0:
        completed_lessons = db.query(LessonProgress).join(
            LessonProgress.lesson
        ).join(
            Lesson.module
        ).filter(
            LessonProgress.user_id == current_user.id,
            LessonProgress.is_completed == True,
            Lesson.module.has(course_id=course_id)
        ).count()
        
        exact_progress = (completed_lessons / total_lessons) * 100
        enrollment.progress = round(exact_progress, 2)
        db.commit()
    
    return {
        "course_id": course_id,
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "progress": round((completed_lessons / total_lessons) * 100, 2) if total_lessons > 0 else 0,
        "is_completed": enrollment.completed
    }

# ==================== UPDATE COURSE PROGRESS ====================
@router.put("/courses/{course_id}/progress")
def update_course_progress(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check enrollment
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Not enrolled in this course")
    
    # ✅ Recalculate exact progress
    total_lessons = db.query(Lesson).join(Lesson.module).filter(
        Lesson.module.has(course_id=course_id)
    ).count()
    
    if total_lessons > 0:
        completed_lessons = db.query(LessonProgress).join(
            LessonProgress.lesson
        ).join(
            Lesson.module
        ).filter(
            LessonProgress.user_id == current_user.id,
            LessonProgress.is_completed == True,
            Lesson.module.has(course_id=course_id)
        ).count()
        
        exact_progress = (completed_lessons / total_lessons) * 100
        enrollment.progress = round(exact_progress, 2)
        
        if exact_progress >= 100:
            enrollment.completed = True
            enrollment.completed_at = datetime.utcnow()
        
        db.commit()
    
    return {
        "course_id": course_id,
        "progress": enrollment.progress,
        "is_completed": enrollment.completed
    }

# ==================== RECALCULATE PROGRESS (NEW) ====================
@router.post("/courses/{course_id}/recalculate")
def recalculate_progress(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Recalculate course progress based on completed lessons"""
    
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Not enrolled")
    
    # ✅ Count total lessons
    total_lessons = db.query(Lesson).join(Lesson.module).filter(
        Lesson.module.has(course_id=course_id)
    ).count()
    
    if total_lessons == 0:
        return {"message": "No lessons in this course", "progress": 0}
    
    # ✅ Count completed lessons
    completed_lessons = db.query(LessonProgress).join(
        LessonProgress.lesson
    ).join(
        Lesson.module
    ).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.is_completed == True,
        Lesson.module.has(course_id=course_id)
    ).count()
    
    # ✅ Update progress
    progress = round((completed_lessons / total_lessons) * 100, 2)
    enrollment.progress = progress
    
    if progress >= 100:
        enrollment.completed = True
        enrollment.completed_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "course_id": course_id,
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "progress": progress,
        "is_completed": enrollment.completed
    }
# ==================== GET COMPLETED LESSONS ====================
@router.get("/courses/{course_id}/completed-lessons")
def get_completed_lessons(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of completed lesson IDs for a course"""
    
    # Check enrollment
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Not enrolled in this course")
    
    # ✅ Get completed lesson IDs
    completed_lessons = db.query(LessonProgress).join(
        LessonProgress.lesson
    ).join(
        Lesson.module
    ).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.is_completed == True,
        Lesson.module.has(course_id=course_id)
    ).all()
    
    return [lp.lesson_id for lp in completed_lessons]