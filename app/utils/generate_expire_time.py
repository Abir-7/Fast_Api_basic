from datetime import datetime, timedelta, timezone

def gen_exp_time(minutes: int = 10) -> datetime:
    """
    Generate a timezone-aware UTC expiration time.
    Defaults to 10 minutes if no argument is passed.
    """
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)