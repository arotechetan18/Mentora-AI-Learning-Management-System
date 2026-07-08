from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...core.security import get_current_user
from ...models.user import User
from ...models.course import Course
from ...models.enrollment import Enrollment
from ...schemas.enrollment import EnrollmentCreate, EnrollmentResponse

router = APIRouter(tags=["Enrollments"])

# ==================== ENROLL IN COURSE ====================
@router.post("/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_in_course(
    enrollment_data: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Enroll a student in a course
    """
    # Check if course exists
    course = db.query(Course).filter(Course.id == enrollment_data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if already enrolled
    existing = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == enrollment_data.course_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")
    
    # Create enrollment
    new_enrollment = Enrollment(
        user_id=current_user.id,
        course_id=enrollment_data.course_id
    )
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment

# ==================== GET MY ENROLLMENTS ====================
@router.get("/enrollments", response_model=List[EnrollmentResponse])
def get_my_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all courses the current user is enrolled in
    """
    enrollments = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id
    ).all()
    return enrollments

# ==================== CHECK ENROLLMENT STATUS ====================
@router.get("/enrollments/{course_id}/check", response_model=bool)
def check_enrollment(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Check if current user is enrolled in a course
    """
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()
    return enrollment is not None

# ==================== UNENROLL FROM COURSE ====================
@router.delete("/enrollments/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def unenroll_from_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Unenroll from a course
    """
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Not enrolled in this course")
    
    db.delete(enrollment)
    db.commit()
    return {"message": "Unenrolled successfully"}