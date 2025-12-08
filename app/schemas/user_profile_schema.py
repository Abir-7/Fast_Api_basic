from pydantic import BaseModel

class CreateUserProfile(BaseModel):   
    full_name: str
    age: int