from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    """Base user model (shared fields)"""
    username: str
    full_name: Optional[str] = None
    email: EmailStr  # Ensures email format is valid

class UserCreate(UserBase):
    """User creation model (requires password)"""
    password: str

class User(UserBase):
    """User model returned by API (includes role & ID)"""
    _id: Optional[str] = None  # MongoDB ObjectId
    role: str = "user"  # Default role is 'user'

    class Config:
        orm_mode = True  # Allows compatibility with ORM-like libraries