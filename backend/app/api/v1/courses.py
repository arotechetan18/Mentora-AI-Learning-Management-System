from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.database import get_db
from ...core.security import get_current_user, get_current_instructor_or_admin
from ...models.user import User
from ...models.course import Course, DifficultyLevel
from ...schemas.course import CourseCreate, CourseUpdate, CourseResponse

router = APIRouter(tags=["Courses"])

@router.post("/courses", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin)
):
    new_course = Course(
        **course_data.model_dump(),
        instructor_id=current_user.id
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.get("/courses", response_model=List[CourseResponse])
def list_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    difficulty: Optional[DifficultyLevel] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # query = db.query(Course).filter(Course.is_published == True)   #AJUN COURCE ACESS NAHI 
    query = db.query(Course)   #COURCE ACESS
    if category:
        query = query.filter(Course.category == category)
    if difficulty:
        query = query.filter(Course.difficulty == difficulty)
    if search:
        query = query.filter(
            Course.title.ilike(f"%{search}%") | 
            Course.description.ilike(f"%{search}%")
        )
    
    courses = query.offset(skip).limit(limit).all()
    return courses

@router.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/courses/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course_update: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if current_user.role != "admin" and course.instructor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    for field, value in course_update.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    
    db.commit()
    db.refresh(course)
    return course

@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if current_user.role != "admin" and course.instructor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}