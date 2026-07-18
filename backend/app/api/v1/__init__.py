from .auth import router as auth_router
from .courses import router as courses_router
from .enrollments import router as enrollments_router
from .notes import router as notes_router
from .quizzes import router as quizzes_router
from .ai_doubt import router as ai_doubt_router
from .progress import router as progress_router
from .lessons import router as lessons_router
from .modules import router as modules_router


__all__ = [
    "auth_router", "courses_router", "enrollments_router",
    "notes_router", "quizzes_router", "ai_doubt_router",
    "progress_router", "lessons_router", "modules_router"
]