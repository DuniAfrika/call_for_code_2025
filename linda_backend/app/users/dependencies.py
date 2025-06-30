from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session
from .utils import verify_password, get_password_hash
from app.db.models import TokenData
from .models import User
from app.db.config import get_session
from typing import Optional
import os

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Get database session
def get_db():
    """
    Dependency to get a database session.
    """
    db = next(get_session())
    try:
        yield db
    finally:
        db.close()

def create_user(db: Session, user: User) -> User:
    """
    Create a new user in the database.
    """
    user.hashed_password = get_password_hash(user.hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, phone: str) -> Optional[User]:
    return db.query(User).where(User.phone == phone).first()

def authenticate_user(db: Session, phone: str, password: str) -> Optional[User]:
    user = get_user(db, phone)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        phone: str = payload.get("sub")
        if phone is None:
            raise credentials_exception
        token_data = TokenData(phone=phone)
    except JWTError:
        raise credentials_exception
    
    user = get_user(db, phone=token_data.phone)
    if user is None:
        raise credentials_exception
    return user