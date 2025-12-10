from fastapi import APIRouter,Depends,BackgroundTasks
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.user_schema import CreateUserWithProfile ,UserRead ,UserLogin
from app.schemas.user_verification_schema import verifyUser
from app.core.database import get_session
from app.service.user_service import UserService
from app.schemas.api_response_model.user_login import LoginResponse
router=APIRouter(prefix="/users",tags=["users"])

@router.post('/signup', response_model=UserRead )
async def create_user(
    data:CreateUserWithProfile,  background_tasks: BackgroundTasks,db:AsyncSession=Depends(get_session),
):
        user = await UserService.create_user_with_profile(db, data,background_tasks)
        return user

@router.post("/verify-user")
async def verify_user(
        data:verifyUser,db:AsyncSession=Depends(get_session)
):
        result=await UserService.verifyUser(db,data.user_id,data.code)
        return result

@router.post('/login', response_model=LoginResponse)
async def userLogin(data:UserLogin,db:AsyncSession=Depends(get_session)):
          return await UserService.userLogin(db,data.email,data.password)