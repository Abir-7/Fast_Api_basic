from pydantic import BaseModel,field_validator,EmailStr

from app.schemas.user_profile_schema import CreateUserProfile
from uuid import UUID
from typing import Optional
from app.enums.user_enum import AccountStatus


class CreateUser(BaseModel):   
    email: EmailStr
    password: str
    @field_validator("email")
    def normalize_email(cls, v: str): 
        return v.strip().lower()

class CreateUserWithProfile(BaseModel):
    email: str
    password: str
    profile:CreateUserProfile
    @field_validator("email")
    def normalize_email(cls, v:str):
        return v.strip().lower()



class UserProfileRead(BaseModel):
    id: UUID
    full_name: str
    age: int

class UserRead(BaseModel):
    user_id: UUID
    message: str
    

class UserLogin(BaseModel):
    email:str
    password:str

class ResendCode(BaseModel):
    user_id: UUID

class RequestForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    user_id: UUID
    new_password:str
    confirm_password:str
    token:str


class UserUpdate(BaseModel):
    password: Optional[str] = None
    account_status: Optional[AccountStatus] = None
    is_verified: Optional[bool] = None
    need_to_reset_password: Optional[bool] = None
