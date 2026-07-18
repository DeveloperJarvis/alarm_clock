from datetime import datetime


def parse_time(value: str) -> tuple[int, int]:
    """
    Convert HH:MM into hour and minute
    """
    
    try:
        hour, minute = value.split(":")
        hour = int(hour)
        minute = int(minute)
    
    except Exception:
        raise ValueError(
            "Time must be in HH:MM format"
        )
    
    if not (
        0 <= hour <= 23
        and 0 <= minute <= 60
    ):
        raise ValueError(
            "Invalid time"
        )
    
    return hour, minute


def format_time(hour: int, minute: int):
    return f"{hour:02d}:{minute:02d}"


def now():
    return datetime.now()
