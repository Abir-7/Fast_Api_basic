from pydantic import BaseModel
from typing import Optional
from app.schemas.user_profile_schema import CreateUserProfile
from uuid import UUID

class CreateUser(BaseModel):   
    email: str
    password: str

class CreateUserWithProfile(BaseModel):
    email: str
    password: str
    profile:CreateUserProfile



class UserProfileRead(BaseModel):
    id: UUID
    full_name: str
    age: int

class UserRead(BaseModel):
    user_id: UUID
    message: str
    

