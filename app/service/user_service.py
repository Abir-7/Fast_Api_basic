from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.request.user_request_schema import UpdateUserProfile
from fastapi import HTTPException,status
from app.repository.user_repository import UserRepository
from uuid import UUID
from app.models.user_profile_model import UserProfile

class UserService:
    @staticmethod
    async def update_user_profile(db:AsyncSession,data:UpdateUserProfile,user_id:UUID)->UserProfile:
        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided for update"
            )
        
        profile = await UserRepository.update_user_profile(
            session=db,
            data=update_data,     user_id=user_id,
        )

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        await db.commit()
        return profile