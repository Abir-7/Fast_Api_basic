from sqlmodel import Field
from sqlalchemy import Column, DateTime
from datetime import datetime, timezone

def TimestampField(default_now=True, update_on_change=False):
    """
    Helper to create a timezone-aware timestamp field for SQLModel models.

    :param default_now: If True, sets default to current UTC time
    :param update_on_change: If True, sets onupdate to current UTC time
    """
    kwargs = {}
    if default_now:
        kwargs['default_factory'] = lambda: datetime.now(timezone.utc)
        sa_kwargs = {
            'nullable': False,
            'default': lambda: datetime.now(timezone.utc)
        }
    else:
        sa_kwargs = {}

    if update_on_change:
        sa_kwargs['onupdate'] = lambda: datetime.now(timezone.utc)

    return Field(sa_column=Column(DateTime(timezone=True), **sa_kwargs), **kwargs)
