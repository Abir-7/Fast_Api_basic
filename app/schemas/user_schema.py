from pydantic import BaseModel,field_validator

from app.schemas.user_profile_schema import CreateUserProfile
from uuid import UUID

class CreateUser(BaseModel):   
    email: str
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