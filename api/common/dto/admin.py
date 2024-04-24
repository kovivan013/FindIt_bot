from typing import Optional, Dict, Any
from schemas.schemas import AnnouncementDetails
from pydantic import BaseModel


class AdminAdd(BaseModel):

    permissions: Dict[str, bool] = {}


class PermissionsUpdate(BaseModel):

    permissions: Dict[str, bool] = {}

class UserBan(BaseModel):

    administrator: int = 0
    reason: str = ""
    duration: int = 0