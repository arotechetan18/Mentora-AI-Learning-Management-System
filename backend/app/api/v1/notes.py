from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from datetime import datetime
from ...core.database import get_db
from ...core.security import get_current_user, get_current_instructor_or_admin
from ...models.user import User
from ...models.course import Course
from ...models.note import Note
from ...schemas.note import NoteCreate, NoteResponse

router = APIRouter(tags=["Notes"])

# Upload directory
UPLOAD_DIR = "uploads/notes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ==================== UPLOAD NOTE ====================
@router.post("/courses/{course_id}/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def upload_note(
    course_id: int,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin)
):
    """
    Upload a note for a course (Instructor/Admin only)
    """
    # Check if course exists
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check permission
    if current_user.role != "admin" and course.instructor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to upload notes for this course")
    
    # Validate file type
    allowed_types = ["pdf", "ppt", "pptx", "doc", "docx", "txt", "md"]
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in allowed_types:
        raise HTTPException(status_code=400, detail=f"File type not allowed. Allowed: {allowed_types}")
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Get file size
    file_size = os.path.getsize(file_path)
    
    # Create note in database
    new_note = Note(
        title=title,
        description=description,
        file_url=file_path,
        file_type=file_extension,
        file_size=file_size,
        course_id=course_id,
        uploaded_by=current_user.id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    
    return new_note

# ==================== GET NOTES ====================
@router.get("/courses/{course_id}/notes", response_model=List[NoteResponse])
def get_course_notes(
    course_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all notes for a course
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    notes = db.query(Note).filter(Note.course_id == course_id).all()
    return notes

# ==================== GET SINGLE NOTE ====================
@router.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    """
    Get note by ID
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# ==================== DOWNLOAD NOTE ====================
@router.get("/notes/{note_id}/download")
def download_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    """
    Download note file
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Check if file exists
    if not os.path.exists(note.file_url):
        raise HTTPException(status_code=404, detail="File not found on server")
    
    return FileResponse(
        path=note.file_url,
        filename=os.path.basename(note.file_url),
        media_type="application/octet-stream"
    )

# ==================== DELETE NOTE ====================
@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_instructor_or_admin)
):
    """
    Delete a note (Instructor/Admin only)
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Check permission
    if current_user.role != "admin" and note.uploaded_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this note")
    
    # Delete file from server
    try:
        if os.path.exists(note.file_url):
            os.remove(note.file_url)
    except Exception:
        pass  # Continue even if file deletion fails
    
    # Delete from database
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}

# ==================== BOOKMARK NOTE ====================
@router.put("/notes/{note_id}/bookmark", response_model=NoteResponse)
def toggle_bookmark(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Toggle bookmark status for a note
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note.is_bookmarked = not note.is_bookmarked
    db.commit()
    db.refresh(note)
    return note