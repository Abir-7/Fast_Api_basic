from sqlmodel import SQLModel, Field, Relationship ,Column,Enum,String

from typing import Optional, TYPE_CHECKING
from uuid import uuid4, UUID
from app.models.user_authentication_model import UserAuthentication
from app.enums.user_enum import UserRole
# Only for type hinting, avoids circular import
if TYPE_CHECKING:
    from app.models.user_profile_model import UserProfile

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True,index=True)
    email: str =Field( sa_column=Column(String, unique=True, index=True))
    password: str
    role:UserRole= Field(
        default=UserRole.USER, 
        sa_column=Column(Enum(UserRole))
    )
    # Use a string for forward reference
    profile: Optional["UserProfile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False,}, cascade_delete=True
    )
    user_authentication:"UserAuthentication" =Relationship(
        back_populates="user"
        ,cascade_delete=True
    )


