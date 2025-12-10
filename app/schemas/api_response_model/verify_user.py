from pydantic import BaseModel
from typing import Optional

class VerifyUserResponse(BaseModel):
    user_id: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token: Optional[str] = None
