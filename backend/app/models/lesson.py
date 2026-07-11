from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    # 4 Parts
    concept = Column(Text, nullable=True)              # 📖 Theory
    example = Column(Text, nullable=True)              # 💡 Real-life + Code
    interview_questions = Column(Text, nullable=True)  # 🎯 Interview Qs
    
    duration = Column(Integer, default=0)
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    module = relationship("Module", back_populates="lessons")
    quiz_questions = relationship("QuizQuestion", back_populates="lesson", cascade="all, delete-orphan")