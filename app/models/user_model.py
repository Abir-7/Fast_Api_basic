from sqlmodel import SQLModel, Field, Relationship ,Column,Enum,String
from datetime import datetime
from app.core.db_time_field import TimestampField
from typing import Optional, TYPE_CHECKING
from uuid import uuid4, UUID
from app.models.user_authentication_model import UserAuthentication
from app.enums.user_enum import UserRole, AccountStatus


# Only for type hinting, avoids circular import
if TYPE_CHECKING:
    from app.models.user_profile_model import UserProfile

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True,index=True)
    email: str =Field( sa_column=Column(String, unique=True, index=True))
    is_verified:bool=Field(default=False)
    account_status:AccountStatus = Field(default=AccountStatus.pending,
    sa_column=Column(Enum(AccountStatus,
    )))
    password: str
    role:UserRole= Field(
        default=UserRole.USER, 
        sa_column=Column(Enum(UserRole))
    )
    created_at: datetime = TimestampField()
    updated_at: datetime = TimestampField(update_on_change=True)
    # Use a string for forward reference
    profile: Optional["UserProfile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False,}, cascade_delete=True
    )
    user_authentication:"UserAuthentication" =Relationship(
        back_populates="user"
        ,cascade_delete=True
    )


