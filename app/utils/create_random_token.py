import secrets

def create_random_token(length: int = 10) -> str:
    return secrets.token_urlsafe(length)