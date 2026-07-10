from .auth import router as auth_router
from .courses import router as courses_router
from .enrollments import router as enrollments_router
from .notes import router as notes_router
from .quizzes import router as quizzes_router
from .ai_doubt import router as ai_doubt_router

__all__ = [
    "auth_router", "courses_router", "enrollments_router",
    "notes_router", "quizzes_router", "ai_doubt_router"
]