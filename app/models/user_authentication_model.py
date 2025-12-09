from sqlmodel import SQLModel, Field, Relationship,Column,Enum, DateTime
from typing import TYPE_CHECKING
from uuid import uuid4, UUID
from typing import Optional
from datetime import datetime ,timezone
from app.enums.user_enum import AuthenticationStatus
from app.core.db_time_field import TimestampField
if TYPE_CHECKING:
    from app.models.user_model import User

class UserAuthentication(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id",ondelete="CASCADE")
    code:Optional[str]=Field(default=None)
    expire_time:datetime= Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    token:Optional[str]=Field(default=None)
    authentication_status:AuthenticationStatus= Field(
        default=AuthenticationStatus.pending, 
        sa_column=Column(Enum(AuthenticationStatus))
    )
    user: "User" = Relationship(back_populates="user_authentication",)
     # Timestamp fields
    created_at: datetime = TimestampField()
    updated_at: datetime = TimestampField(update_on_change=True)