from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class Note(Base):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    file_url = Column(String, nullable=False)  # File path
    file_type = Column(String, nullable=False)  # pdf, ppt, doc, etc.
    file_size = Column(Integer, nullable=True)  # File size in bytes
    course_id = Column(Integer, ForeignKey("courses.id"))
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    is_bookmarked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    course = relationship("Course", backref="notes")
    uploader = relationship("User", backref="notes_uploaded")