from sqlmodel import SQLModel, Field, Relationship # type: ignore
from typing import TYPE_CHECKING
from uuid import uuid4, UUID
from datetime import datetime
from app.core.db_time_field import TimestampField

if TYPE_CHECKING:
    from app.models.user_model import User

class UserProfile(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id",ondelete="CASCADE")
    full_name: str
    age: int

    # Forward reference as string
    user: "User" = Relationship(back_populates="profile",)
    created_at: datetime = TimestampField()
    updated_at: datetime = TimestampField(update_on_change=True)