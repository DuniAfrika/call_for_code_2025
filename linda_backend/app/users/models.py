import uuid
from typing import Optional
from pydantic import SecretStr, EmailStr
from sqlmodel import SQLModel
from sqlmodel import Field
from app.db.models import UserBase

class UserRegister(UserBase):
    password: SecretStr

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str

class UserUpdate(SQLModel):
    username: Optional[str] = Field(None, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    isAdmin: Optional[bool] = None
    isActive: Optional[bool] = None

class UserPublic(UserBase):
    id: uuid.UUID
    username: str
    email: EmailStr
    phone: str
    full_name: Optional[str] = None
    isAdmin: bool
    isActive: bool

class UserLogin(SQLModel):
    phone: str
    password: SecretStr