from typing import Optional, Dict, Any
from schemas.schemas import AnnouncementDetails
from pydantic import BaseModel


class AdminAdd(BaseModel):

    permissions: Dict[str, bool] = {}


class PermissionsUpdate(BaseModel):

    permissions: Dict[str, bool] = {}


class UserBan(BaseModel):

    reason: str = ""
    duration: int = 0