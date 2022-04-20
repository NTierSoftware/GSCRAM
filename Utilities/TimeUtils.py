from datetime import datetime


def millisSinceMidnight() -> int:
    now = datetime.utcnow()
    diff = now - now.replace(hour=0, minute=0, second=0, microsecond=0)
    return round(diff.total_seconds() * 1000, None)


# def millisSinceMidnightUTC() -> int:
#     now = datetime.utcnow()
#     diff = now - now.replace(hour=0, minute=0, second=0, microsecond=0)
#     return round(diff.total_seconds() * 1000, None)
