from pydantic import BaseModel
from uuid import UUID
class SignupResponse(BaseModel):
    user_id: UUID 
    message:str
