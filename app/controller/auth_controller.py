from fastapi import APIRouter,Depends,BackgroundTasks
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.request.auth_request_schema import CreateUserWithProfile  ,UserLogin,ResendCode ,RequestForgotPassword, ResetPassword

from app.core.database import get_session
from app.service.auth_service import AuthService
from app.schemas.response.auth_response_schema import SignupResponse,UserIdResponse,VerifyUserEmailResponse,VerifyUserResetPasswordResponse,LoginResponse , NewAccessTokenResponse
from typing import Union
from app.schemas.request.auth_request_schema import VerifyUser ,NewAccessToken


router=APIRouter(prefix="/auth",tags=["auth"])

@router.post('/signup', response_model=SignupResponse )
async def create_user(
    data:CreateUserWithProfile,  background_tasks: BackgroundTasks,db:AsyncSession=Depends(get_session)
):
        result = await AuthService.create_user_with_profile(db, data,background_tasks)
        return result

@router.post("/verify-user",response_model=Union[VerifyUserEmailResponse,VerifyUserResetPasswordResponse])
async def verify_user(
        data:VerifyUser,db:AsyncSession=Depends(get_session)
):
        result=await AuthService.verifyUser(db,data.user_id,data.code)
        return result

@router.post('/login', response_model=LoginResponse)
async def userLogin(data:UserLogin,db:AsyncSession=Depends(get_session)
):
        result=await AuthService.userLogin(db,data.email,data.password)
        return result

@router.post('/resend', response_model=UserIdResponse)
async def resendCode(data:ResendCode,db:AsyncSession=Depends(get_session)
):
        result=await AuthService.resendCode(db,str(data.user_id))
        return result

@router.post('/request-for-reset-password',response_model=UserIdResponse)
async def reqForResetPassword(data:RequestForgotPassword,background_tasks: BackgroundTasks,db:AsyncSession=Depends(get_session)
):
        result=await AuthService.forgotPasswordRequest(db=db,user_email=data.email,background_tasks=background_tasks)    
        return result

@router.post('/reset-password')
async def resetPassword(data:ResetPassword,db:AsyncSession=Depends(get_session)
):
        result=await AuthService.resetPassword(db=db,data=data)
        return result

@router.post('/get-new-access-token')
async def reqNewAccessToken(data:NewAccessToken
)->NewAccessTokenResponse:
        result= AuthService.getNewAccessToken(refresh_token=data.refresh_token)
        return result

        