from pydantic import BaseModel


class verifyUser(BaseModel):   
    user_id: str
    code: str

