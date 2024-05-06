from typing import Optional, Dict, Any
from pydantic import BaseModel


class UserCreate(BaseModel):

    telegram_id: int = 0
    username: str = ""
    description: Optional[str] = ""
    phone_number: int = 0


class UserUpdate(BaseModel):

    username: Optional[str] = ""
    description: Optional[str] = ""
    phone_number: Optional[int] = 0


class NotificationSend(BaseModel):

    preview: str = ""
    text: str = ""
    markup_type: int = 0

