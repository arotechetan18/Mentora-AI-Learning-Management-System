from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    current_lesson = Column(String, nullable=True)
    completion_percentage = Column(Float, default=0.0)
    study_time = Column(Integer, default=0)
    last_studied = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="progress_records")
    course = relationship("Course", backref="progress_records")