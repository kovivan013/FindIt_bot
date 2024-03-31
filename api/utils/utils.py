from datetime import datetime
from uuid import uuid4

def timestamp() -> int:
    return int(
        datetime.now().timestamp()
    )

def _uuid() -> str:
    return str(
        uuid4()
    )

