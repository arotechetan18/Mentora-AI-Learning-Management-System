from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.database import get_db
from ...core.security import get_current_user
from ...models.user import User
from ...models.course import Course
from ...models.ai_chat import AIChat
from ...services.ai_service import AIService
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(tags=["AI Doubt"])

class DoubtQuestion(BaseModel):
    question: str
    course_id: Optional[int] = None

class DoubtResponse(BaseModel):
    question: str
    answer: str
    timestamp: str
    course_id: Optional[int]

class ChatHistoryResponse(BaseModel):
    id: int
    question: str
    answer: str
    created_at: str

@router.post("/ai/doubt", response_model=DoubtResponse)
def ask_doubt(
    doubt: DoubtQuestion,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if course exists and user is enrolled
    if doubt.course_id:
        course = db.query(Course).filter(Course.id == doubt.course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
    
    # Get AI response
    ai_service = AIService()
    answer = ai_service.get_answer(doubt.question)
    
    # Save to history
    chat = AIChat(
        user_id=current_user.id,
        question=doubt.question,
        answer=answer,
        course_id=doubt.course_id
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    
    return DoubtResponse(
        question=doubt.question,
        answer=answer,
        timestamp=str(chat.created_at),
        course_id=doubt.course_id
    )

@router.get("/ai/history", response_model=List[ChatHistoryResponse])
def get_chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chats = db.query(AIChat).filter(
        AIChat.user_id == current_user.id
    ).order_by(AIChat.created_at.desc()).limit(50).all()
    
    return [{
        "id": c.id,
        "question": c.question,
        "answer": c.answer[:200] + "..." if len(c.answer) > 200 else c.answer,
        "created_at": str(c.created_at)
    } for c in chats]

@router.delete("/ai/history/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = db.query(AIChat).filter(
        AIChat.id == chat_id,
        AIChat.user_id == current_user.id
    ).first()
    
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    db.delete(chat)
    db.commit()
    return {"message": "Chat deleted successfully"}