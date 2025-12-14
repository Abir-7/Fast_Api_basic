from app.utils.jwt import decode_token
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from fastapi import Depends,HTTPException,status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from app.schemas.internal.jwt_token_schema import JwtPayload
from typing import Optional,List
from app.models.user_model import User
from uuid import UUID
from sqlmodel import select
from app.enums.user_enum import AccountStatus ,UserRole

security=HTTPBearer()

async def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security),session:AsyncSession=Depends(get_session))-> User:

    if credentials.scheme.lower() !='bearer':
        raise HTTPException(status_code=401,detail="Invalid authentication scheme")
    payload:Optional[JwtPayload] =  decode_token(credentials.credentials)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id=payload['user_id']

    result = await session.exec(
    select(User).where(User.id == UUID(user_id))
    )
    user = result.one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    if user.account_status != AccountStatus.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not active",
        )
    
    return user


def require_roles(roles: List[UserRole]):
    async def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker
