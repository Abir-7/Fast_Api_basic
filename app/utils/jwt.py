# app/utils/jwt_utils.py
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from app.core.config import settings
from app.schemas.function_return_schema.jwt_token_schema import AccessRefreshToken,JwtPayload
# Secret keys — keep them safe and load from env in production

ACCESS_SECRET_KEY: str = settings.ACCESS_TOKEN_SECRET
REFRESH_SECRET_KEY: str = settings.REFRESH_TOKEN_SECRET

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_DAYS = 30
REFRESH_TOKEN_EXPIRE_DAYS = 90

class TokenType:
    ACCESS = "access"
    REFRESH = "refresh"

def create_token(payload: dict[str, Any], token_type: str = TokenType.ACCESS) -> str:
    """
    Create a JWT token (access or refresh) with expiry.
    payload: dict containing user info (e.g., user_id, email, role)
    token_type: "access" or "refresh"
    """
    now = datetime.now(timezone.utc)
    if token_type == TokenType.ACCESS:
        expire = now + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        secret = ACCESS_SECRET_KEY
    elif token_type == TokenType.REFRESH:
        expire = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        secret = REFRESH_SECRET_KEY
    else:
        raise ValueError("Invalid token type")

    token_payload = payload.copy()
    token_payload.update({"exp": expire, "iat": now, "type": token_type})
    token = jwt.encode(token_payload, secret, algorithm=ALGORITHM) # type: ignore
    return token

def decode_token(token: str, token_type: str = TokenType.ACCESS) -> Optional[JwtPayload]:
    """
    Decode a JWT token. Returns the payload if valid, None if invalid/expired.
    """
    try:
        secret = ACCESS_SECRET_KEY if token_type == TokenType.ACCESS else REFRESH_SECRET_KEY
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM]) # type: ignore
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def verify_token(token: str, token_type: str = TokenType.ACCESS) -> bool:
    """
    Simply check if the token is valid and not expired.
    """
    payload = decode_token(token, token_type)
    return payload is not None

def create_access_refresh_tokens(payload: dict[str, Any]) -> AccessRefreshToken:
    """
    Helper to generate both access and refresh tokens at once
    """
    return {
        "access_token": create_token(payload, TokenType.ACCESS),
        "refresh_token": create_token(payload, TokenType.REFRESH)
    }
