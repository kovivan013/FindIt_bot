import requests
import jwt
from typing import Union

from datetime import datetime
import datetime as datetime_module
from common.schemas import BaseAnnouncement
# from common.interfaces import OAuthStructure
# from config import settings


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


def announcement_caption(
        announcement: BaseAnnouncement
) -> str:
    return f"{announcement.title}\n\n" \
           f"" \
           f"📍 *{announcement.location.place_name}*\n" \
           f"⌚ *{to_date(announcement.timestamp)}*"

def announcement_details(
        announcement: BaseAnnouncement
) -> str:
    n = "\n"
    modes: dict = {
        0: {
            0: "Загублено",
            1: "Знайдено"
        },
        1: {
            0: "загублену",
            1: "знайдену"
        }
    }

    return f"{modes[0][announcement.mode]} *{announcement.title}*\n\n" \
           f"" \
           f"{announcement.description}\n\n" \
           f"" \
           f"Інформація про {modes[1][announcement.mode]} річ:\n\n" \
           f"📅 {to_date(announcement.timestamp, with_time=True)}\n" \
           f"🗺 {announcement.location.place_type} {announcement.location.place_name}\n" \
           f"" \
           f"{f'{n}#' + ' #'.join(announcement.tags) + f'{n}{n}' if announcement.tags else n}" \
           f"" \
           f"🌟 *Вам знайома ця річ?* Про натисніть кнопку нижче."

def collect_place(
        location: dict,
        case: int = 0
) -> dict:
    address = location["address"]
    keys: dict = {
        "city": {
            0: "місто",
            1: "міста"
        },
        "town": {
            0: "місто",
            1: "міста"
        },
        "village": {
            0: "село",
            1: "села"
        },
        "municipality": {
            0: ""
        }
    }

    for i, v in keys.items():
        if i in address.keys():
            return {
                "place_type": v[case] if v[case] else "",
                "place_name": address[i]
            }

class TextFilter:

    def __init__(
            self,
            text: str
    ) -> None:
        self.text = text

    def _lenght_equals(
            self,
            value: int
    ) -> bool:
        if value is None: return True
        return len(self.text) == value

    def _min_lenght(
            self,
            value: int,
    ) -> bool:
        if value is None: return True
        return len(self.text) >= value

    def _max_lenght(
            self,
            value: int,
    ) -> bool:
        if value is None: return True
        return len(self.text) <= value

    def _in(
            self,
            value: Union[str, list]
    ) -> bool:
        if value is None: return True
        for i in self.text:
            if i in value:
                return True
        else:
            return False

    def _not_in(
            self,
            value: Union[str, list]
    ) -> bool:
        if value is None: return True
        for i in self.text:
            if i not in value:
                return True
        else:
            return False

    def check(
            self,
            _lenght_equals: int = None,
            _min_lenght: int = None,
            _max_lenght: int = None,
            _in: Union[str, list] = None,
            _not_in: Union[str, list] = None
    ) -> bool:
        return all(
            [
                self._lenght_equals(_lenght_equals),
                self._min_lenght(_min_lenght),
                self._max_lenght(_max_lenght),
                self._in(_in),
                self._not_in(_not_in)
            ]
        )
#
# from common.classes import Symbols
# print(TextFilter("Ыыыыы")._not_in(Symbols.MAIN_SYMBOLS))