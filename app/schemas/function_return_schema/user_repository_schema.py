from typing import TypedDict

class VerifyUserEmailResult(TypedDict):
    user_id: str


class VerifyResetPassResult(TypedDict):
    user_id:str
    token:str