from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.api.v1.auth import router as auth_router
from app.api.v1.courses import router as courses_router
from app.api.v1.enrollments import router as enrollments_router
from app.api.v1.notes import router as notes_router
from app.api.v1.quizzes import router as quizzes_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(courses_router, prefix=settings.API_V1_STR)
app.include_router(enrollments_router, prefix=settings.API_V1_STR)
app.include_router(notes_router, prefix=settings.API_V1_STR)
app.include_router(quizzes_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "AI LMS Backend Running Successfully"}

@app.get("/health")
def health():
    return {"status": "healthy"}