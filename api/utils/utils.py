from datetime import datetime

def timestamp() -> int:
    return int(
        datetime.now().timestamp()
    )