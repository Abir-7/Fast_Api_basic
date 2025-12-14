from fastapi import APIRouter,Depends
from app.models.user_profile_model import UserProfile
from app.schemas.request.user_request_schema import UpdateUserProfile
from app.dependencies.auth import require_roles
from app.enums.user_enum import UserRole
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from app.models.user_model import User
from app.service.user_service import UserService
router=APIRouter(prefix="/user",tags=["user"])

@router.patch("/update-profile",response_model=UserProfile)
async def update_user_profile(data:UpdateUserProfile,current_user:User=Depends(require_roles([UserRole.USER])),db:AsyncSession=Depends(get_session)):
    
    result=await UserService.update_user_profile(db,data,current_user.id)

    return result