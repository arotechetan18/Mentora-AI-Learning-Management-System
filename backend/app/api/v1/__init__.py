from .auth import router as auth_router
from .courses import router as courses_router
from .enrollments import router as enrollments_router

__all__ = ["auth_router", "courses_router", "enrollments_router"]