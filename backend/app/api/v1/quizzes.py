from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime  
from ...core.database import get_db
from ...core.security import get_current_user, get_current_instructor_or_admin
from ...models.user import User
from ...models.course import Course
from ...models.quiz import Quiz, Question, QuizAttempt
from ...schemas.quiz import (
    QuizCreate, QuizUpdate, QuizResponse,
    QuestionResponse, QuizAttemptSubmit, QuizAttemptResponse, QuizResultResponse
)

router = APIRouter(tags=["Quizzes"])

# ==================== CREATE QUIZ ====================
@router.post("/courses/{course_id}/quizzes", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
def create_quiz(
    course_id: int,
    quiz_data: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin)
):
    """
    Create a quiz with questions (Instructor/Admin only)
    """
    # Check if course exists
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check permission
    if current_user.role != "admin" and course.instructor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to create quiz for this course")
    
    # Check if questions exist
    if not quiz_data.questions or len(quiz_data.questions) < 1:
        raise HTTPException(status_code=400, detail="Quiz must have at least 1 question")
    
    # Create quiz
    new_quiz = Quiz(
        title=quiz_data.title,
        description=quiz_data.description,
        course_id=course_id,
        time_limit=quiz_data.time_limit,
        passing_score=quiz_data.passing_score,
        is_published=quiz_data.is_published,
        created_by=current_user.id
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    
    # Create questions
    for q in quiz_data.questions:
        new_question = Question(
            quiz_id=new_quiz.id,
            question_text=q.question_text,
            options=q.options,
            correct_answer=q.correct_answer,
            explanation=q.explanation
        )
        db.add(new_question)
    
    db.commit()
    
    # Refresh quiz with questions
    db.refresh(new_quiz)
    return new_quiz

# ==================== GET COURSE QUIZZES ====================
@router.get("/courses/{course_id}/quizzes", response_model=List[QuizResponse])
def get_course_quizzes(
    course_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all quizzes for a course
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    quizzes = db.query(Quiz).filter(Quiz.course_id == course_id).all()
    return quizzes

# ==================== GET SINGLE QUIZ ====================
@router.get("/quizzes/{quiz_id}", response_model=QuizResponse)
def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db)
):
    """
    Get quiz by ID with all questions
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

# ==================== UPDATE QUIZ ====================
@router.put("/quizzes/{quiz_id}", response_model=QuizResponse)
def update_quiz(
    quiz_id: int,
    quiz_update: QuizUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin)
):
    """
    Update quiz (Instructor/Admin only)
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Check permission
    if current_user.role != "admin" and quiz.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this quiz")
    
    for field, value in quiz_update.model_dump(exclude_unset=True).items():
        setattr(quiz, field, value)
    
    db.commit()
    db.refresh(quiz)
    return quiz

# ==================== DELETE QUIZ ====================
@router.delete("/quizzes/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin)
):
    """
    Delete quiz (Instructor/Admin only)
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Check permission
    if current_user.role != "admin" and quiz.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this quiz")
    
    db.delete(quiz)
    db.commit()
    return {"message": "Quiz deleted successfully"}

# ==================== SUBMIT QUIZ ATTEMPT ====================
@router.post("/quizzes/{quiz_id}/attempt", response_model=QuizAttemptResponse)
def submit_quiz_attempt(
    quiz_id: int,
    attempt_data: QuizAttemptSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit quiz attempt and get auto-graded score
    """
    # Check if quiz exists and is published
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    if not quiz.is_published:
        raise HTTPException(status_code=400, detail="Quiz is not published yet")
    
    # Check if user has already attempted
    existing_attempt = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.quiz_id == quiz_id
    ).first()
    if existing_attempt:
        raise HTTPException(status_code=400, detail="You have already attempted this quiz")
    
    # Get all questions
    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    if not questions:
        raise HTTPException(status_code=400, detail="No questions found in this quiz")
    
    # Check if answers count matches questions count
    if len(attempt_data.answers) != len(questions):
        raise HTTPException(
            status_code=400, 
            detail=f"Please answer all questions. Expected {len(questions)} answers, got {len(attempt_data.answers)}"
        )
    
    # Calculate score
    correct_count = 0
    for i, question in enumerate(questions):
        if attempt_data.answers[i] == question.correct_answer:
            correct_count += 1
    
    total_questions = len(questions)
    score = (correct_count / total_questions) * 100
    passed = score >= quiz.passing_score
    
    # Create attempt with current datetime
    current_time = datetime.utcnow()
    new_attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz_id,
        score=score,
        answers=attempt_data.answers,
        passed=passed,
        completed_at=current_time
    )
    db.add(new_attempt)
    db.commit()
    db.refresh(new_attempt)
    
    return new_attempt

# ==================== GET MY QUIZ ATTEMPTS ====================
@router.get("/quizzes/attempts/my", response_model=List[QuizAttemptResponse])
def get_my_attempts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all quiz attempts by current user
    """
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id
    ).order_by(QuizAttempt.attempted_at.desc()).all()
    return attempts

# ==================== GET QUIZ RESULTS ====================
@router.get("/quizzes/{quiz_id}/results", response_model=QuizResultResponse)
def get_quiz_results(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get results for a specific quiz attempt
    """
    attempt = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.quiz_id == quiz_id
    ).first()
    
    if not attempt:
        raise HTTPException(status_code=404, detail="Quiz attempt not found")
    
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    
    correct_answers = 0
    for i, q in enumerate(questions):
        if attempt.answers[i] == q.correct_answer:
            correct_answers += 1
    
    return {
        "quiz_id": quiz_id,
        "quiz_title": quiz.title,
        "total_questions": len(questions),
        "correct_answers": correct_answers,
        "score": attempt.score,
        "passed": attempt.passed,
        "passing_score": quiz.passing_score,
        "attempt_id": attempt.id,
        "attempted_at": attempt.attempted_at
    }

# ==================== GET ATTEMPT BY ID ====================
@router.get("/attempts/{attempt_id}", response_model=QuizAttemptResponse)
def get_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get quiz attempt by ID
    """
    attempt = db.query(QuizAttempt).filter(QuizAttempt.id == attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    
    if attempt.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to view this attempt")
    
    return attempt