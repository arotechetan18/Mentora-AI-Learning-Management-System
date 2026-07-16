from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine

from app.api.v1.auth import router as auth_router
from app.api.v1.courses import router as courses_router
from app.api.v1.enrollments import router as enrollments_router
from app.api.v1.notes import router as notes_router
from app.api.v1.quizzes import router as quizzes_router
from app.api.v1.ai_doubt import router as ai_doubt_router
from app.api.v1.progress import router as progress_router
from app.api.v1.lessons import router as lessons_router
from app.api.v1.modules import router as modules_router

# Create tables
Base.metadata.create_all(bind=engine)

# Create app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# PERFECT CORS CONFIGURATION - FIXES ALL CORS ISSUES
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:10000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:10000",
        "*"  # Development mode - allow all
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(courses_router, prefix=settings.API_V1_STR)
app.include_router(enrollments_router, prefix=settings.API_V1_STR)
app.include_router(notes_router, prefix=settings.API_V1_STR)
app.include_router(quizzes_router, prefix=settings.API_V1_STR)
app.include_router(ai_doubt_router, prefix=settings.API_V1_STR)
app.include_router(progress_router, prefix=settings.API_V1_STR)
app.include_router(lessons_router, prefix=settings.API_V1_STR)
app.include_router(modules_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "AI LMS Backend Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}