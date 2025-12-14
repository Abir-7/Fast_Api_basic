from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import HTTPException,status
from app.repository.user_repository import UserRepository
from uuid import UUID
from app.models.user_profile_model import UserProfile
from typing import Dict,Any
class UserService:
    @staticmethod
    async def update_user_profile(db:AsyncSession,data:Dict[str,Any],user_id:UUID)->UserProfile:
        
        profile = await UserRepository.update_user_profile(
            session=db,
            data=data   ,  user_id=user_id,
        )
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        await db.commit()
        return profile