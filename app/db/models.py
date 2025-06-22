from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field, create_engine
import uuid


class WhatsAppWebhook(BaseModel):
    to: str
    message: str

database_name = "linda_db.db"
database_path = f"sqlite:///{database_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(database_path, connect_args=connect_args)

class UserBase(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr = Field(unique=True, index=True)
    phone: int = Field(unique=True, index=True)
    isAdmin: bool = True
    isActive: bool = True

class UserRegister(UserBase):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr = Field(unique=True, index=True)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = None

