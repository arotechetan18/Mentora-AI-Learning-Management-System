from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.security import get_password_hash, verify_password, create_access_token
from ...models.user import User, UserRole
from pydantic import BaseModel, EmailStr
from typing import Optional

# ✅ Router instance
router = APIRouter(tags=["Authentication"])  # ✅ हे Add करा

# ==================== TEST ROUTE ====================
@router.get("/test", tags=["Authentication"])  # ✅ हे Add करा
def test():
    return {"message": "Auth Working"}

# ==================== SCHEMAS ====================
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: Optional[UserRole] = UserRole.STUDENT

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# ==================== REGISTER API ====================
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Authentication"])  # ✅ हे Add करा
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role=user_data.role or UserRole.STUDENT
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ==================== LOGIN API ====================
@router.post("/login", response_model=TokenResponse, tags=["Authentication"])  # ✅ हे Add करा
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and get JWT token
    """
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token({"sub": user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }