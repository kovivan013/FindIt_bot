import requests
import jwt

from datetime import datetime
from common.interfaces import OAuthStructure
from config import settings


def timestamp() -> int:
    return int(
        datetime.now().timestamp()
    )

def get_photo(
        filename: str
):
    return open(
        f"images/{filename}",
        "rb"
    )




