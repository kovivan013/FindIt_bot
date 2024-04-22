from typing import Optional, Dict, Any
from schemas.schemas import AnnouncementDetails
from pydantic import BaseModel

class AdminAdd(BaseModel):

    permissions: Dict[str, Any] = {}