from pydantic import BaseModel

from uuid import UUID



class UserIdResponse(BaseModel):
    user_id:UUID

class SignupResponse(BaseModel):
    user_id:UUID
    message:str

class VerifyUserEmailResponse(BaseModel):
    user_id:UUID
    access_token: str
    refresh_token: str 

class VerifyUserResetPasswordResponse(BaseModel):
    user_id:UUID 
    token: str 

class LoginResponse(BaseModel):
    user_id:UUID
    access_token: str
    refresh_token: str


class NewAccessTokenResponse(BaseModel):
    access_token: str


