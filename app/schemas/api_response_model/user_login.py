from pydantic import BaseModel
from uuid import UUID
class LoginResponse(BaseModel):
    user_id: UUID 
    access_token: str
    refresh_token: str
