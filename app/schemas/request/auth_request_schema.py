
from app.schemas.request.user_request_schema import CreateUserProfile
from pydantic import BaseModel,field_validator,EmailStr
from uuid import UUID



class CreateUserWithProfile(BaseModel):
    email: EmailStr
    password: str
    profile:CreateUserProfile
    @field_validator("email")
    def normalize_email(cls, v:str):
        return v.strip().lower()

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


class VerifyUser(BaseModel):   
    user_id: str
    code: str


class NewAccessToken(BaseModel):
    refresh_token:str