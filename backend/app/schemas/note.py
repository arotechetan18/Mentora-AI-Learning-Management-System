from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NoteBase(BaseModel):
    title: str
    description: Optional[str] = None
    file_type: str  # pdf, ppt, doc, etc.

class NoteCreate(NoteBase):
    course_id: int

class NoteResponse(NoteBase):
    id: int
    file_url: str
    file_size: Optional[int]
    course_id: int
    uploaded_by: int
    is_bookmarked: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True