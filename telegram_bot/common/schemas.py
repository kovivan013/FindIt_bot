from pydantic import BaseModel
from typing import Dict, Any


class AnnouncementLocation(BaseModel):

    latitude: float = 0.0
    longitude: float = 0.0
    place_name: str = ""
    place_type: str = ""


class AnnouncementSecrets(BaseModel):

    question: str = ""
    answer: str = ""


class AnnouncementDetails(BaseModel):

    title: str = ""
    description: str = ""
    address: Dict[str, Any] = {}
    timestamp: int = 0
    tags: list = []
    secrets: AnnouncementSecrets = AnnouncementSecrets()
    location: AnnouncementLocation = AnnouncementLocation()