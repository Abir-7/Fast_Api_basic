from fastapi import Form, HTTPException
from pydantic import BaseModel, ValidationError
import json
from typing import Type, TypeVar

T = TypeVar("T", bound=BaseModel)

def validate_form_data(model: Type[T]):
    """
    Dependency to parse a JSON string from a form field 'data' and convert it to a Pydantic model.
    Usage: Depends(json_form(UpdateUserProfile))
    """
    async def dependency(data: str = Form(...)) -> T:
        try:
            data_dict = json.loads(data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON in 'data' field")
        
        try:
            return model(**data_dict)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())
    
    return dependency
