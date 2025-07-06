from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import datetime
from .dependencies import get_current_user, get_db
from .models import User, UserUpdate, UserPublic, UserRegister, UserLogin
from app.db.models import Token
from .utils import create_access_token, get_password_hash, verify_password

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=Token)
async def register_user(user: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    if db.query(User).filter(User.phone == user.phone).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered."
        )
    
    hashed_password = get_password_hash(user.password.get_secret_value())
    db_user = User(
        **user.model_dump(exclude={"password"}),
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_access_token(data={"sub": db_user.phone})

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """
    Login a user and return an access token.
    """
    user_data = db.query(User).filter(User.phone == user.phone).first()
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    password_str = user.password.get_secret_value()
    if not verify_password(password_str, user_data.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user_data.phone})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserPublic)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get the current logged-in user's information.
    """
    return UserPublic.model_validate(current_user)