import requests
import jwt

from datetime import datetime
import datetime as datetime_module
from common.interfaces import OAuthStructure
from config import settings


def timestamp() -> int:
    return int(
        datetime.now().timestamp()
    )

def to_date(
        timestamp: int,
        with_time: bool = False
) -> str:
    now = datetime.now()
    date = datetime.fromtimestamp(timestamp)

    today = all(
        [
            date.year == now.year,
            date.month == now.month,
            date.day == now.day
        ]
    )
    yesterday = all(
        [
            date.year == now.year,
            date.month == now.month,
            date.day == (now - datetime_module.timedelta(
                days=1
            )).day
        ]
    )

    timing = f"{date.hour}:{date.minute if date.minute > 9 else f'0{date.minute}'}"

    if today:
        time = f"Сьогодні, о {timing}"
    elif yesterday:
        time = f"Учора, о {timing}"
    else:
        time = f"{date.day if date.day > 9 else f'0{date.day}'}." \
               f"{date.month if date.month > 9 else f'0{date.month}'}." \
               f"{date.year}{f', о {timing}' if with_time else ''}"

    return time

def get_photo(
        filename: str
):
    return open(
        f"images/{filename}",
        "rb"
    )




