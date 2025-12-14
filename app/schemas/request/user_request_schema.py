from pydantic import BaseModel,field_validator,EmailStr
from typing import Optional
from app.enums.user_enum import AccountStatus


class CreateUser(BaseModel):   
    email: EmailStr
    password: str
    @field_validator("email")
    def normalize_email(cls, v: str): 
        return v.strip().lower()

class CreateUserProfile(BaseModel):   
    full_name: str
    age: int

class UpdateUser(BaseModel):
    password: Optional[str] = None
    account_status: Optional[AccountStatus] = None
    is_verified: Optional[bool] = None
    need_to_reset_password: Optional[bool] = None


class UpdateUserProfile(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    model_config = {
        "extra": "forbid"  # forbid unknown fields
    }