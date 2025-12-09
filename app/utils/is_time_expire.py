from datetime import datetime,timezone

def is_time_expired(expire_time: datetime) -> bool:
    if expire_time.tzinfo is None:
        expire_time = expire_time.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) > expire_time