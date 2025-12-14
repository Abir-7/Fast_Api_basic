from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID
from typing import Optional, Dict, Any

from app.models.user_profile_model import UserProfile


class UserRepository:

    @staticmethod
    async def update_user_profile(
        session: AsyncSession,
        data: Dict[str,Any],
        user_id: UUID
    ) -> Optional[UserProfile]:

        result = await session.exec(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile = result.one_or_none()

        if profile is None:
            return None
        print(data)
        for field, value in data.items():
            setattr(profile, field, value)

        await session.flush()  
        return profile
