from typing import TypedDict
from app.enums.user_enum import UserRole
class AccessRefreshToken(TypedDict):
    access_token:str
    refresh_token:str

class JwtPayload(TypedDict):
    user_id:str
    user_email:str
    user_role:UserRole