from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from uuid import uuid4, UUID

if TYPE_CHECKING:
    from app.models.user_model import User

class UserProfile(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id",ondelete="CASCADE")
    full_name: str
    age: int

    # Forward reference as string
    user: "User" = Relationship(back_populates="profile",)
