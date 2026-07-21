# app/models/profile.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True)
    
    # Personal Info
    bio = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    location = Column(String(100), nullable=True)
    website = Column(String(200), nullable=True)
    
    # Professional Info
    education = Column(Text, nullable=True)
    experience = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    
    # Social Links
    github = Column(String(200), nullable=True)
    linkedin = Column(String(200), nullable=True)
    twitter = Column(String(200), nullable=True)
    youtube = Column(String(200), nullable=True)
    
    # Preferences
    email_notifications = Column(Boolean, default=True)
    course_updates = Column(Boolean, default=True)
    
    # Profile Picture
    avatar_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="profile")