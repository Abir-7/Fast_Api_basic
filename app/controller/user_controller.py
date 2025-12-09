from fastapi import APIRouter,Depends,HTTPException,BackgroundTasks
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.user_schema import CreateUserWithProfile ,UserRead
from app.core.database import get_session
from app.service.user_service import UserService

router=APIRouter(prefix="/users",tags=["users"])

@router.post('/signup', response_model=UserRead)
async def create_user(
    data:CreateUserWithProfile,  background_tasks: BackgroundTasks,db:AsyncSession=Depends(get_session),
):
        user = await UserService.create_user_with_profile(db, data,background_tasks)
        return user
   