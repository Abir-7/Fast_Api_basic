from sqlmodel import SQLModel, Field, Relationship,Column,Enum
from typing import TYPE_CHECKING
from uuid import uuid4, UUID
from typing import Optional
from datetime import datetime
from app.enums.user_enum import AuthenticationStatus

if TYPE_CHECKING:
    from app.models.user_model import User

class UserAuthentication(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id",ondelete="CASCADE")
    code:Optional[str]=Field(default=None)
    expire_time:datetime
    token:Optional[str]=Field(default=None)
    authentication_status:AuthenticationStatus= Field(
        default=AuthenticationStatus.PENDING, 
        sa_column=Column(Enum(AuthenticationStatus))
    )
    user: "User" = Relationship(back_populates="user_authentication",)
