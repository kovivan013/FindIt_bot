from typing import Optional, Dict, Any
from pydantic import BaseModel


class UserCreate(BaseModel):

    telegram_id: int
    username: str
    description: Optional[str] = ""
    badges: Optional[Dict[str, Any]] = {}
    phone_number: int
    mode: int = 0
    announcements: Optional[Dict[str, Any]] = {}
    created_at: int
    updated_at: Optional[int] = 0


class UserUpdate(BaseModel):

    username: str
    description: Optional[str] = ""
    badges: Optional[Dict[str, Any]] = {}
    phone_number: int
    mode: int = 0
    updated_at: Optional[int] = 0