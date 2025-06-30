from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field
import uuid


class WhatsAppWebhook(BaseModel):
    to: str
    message: str

class UserBase(SQLModel):
    __tablename__ = "users"
    username: str = Field(unique=True, index=True, max_length=50)
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr = Field(unique=True, index=True)
    phone: str = Field(unique=True, index=True, max_length=15)
    isAdmin: bool = True
    isActive: bool = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    phone: str | None = None