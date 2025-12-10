from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.user_schema import CreateUserWithProfile
from app.repository.user_repository import UserRepository
from app.models.user_authentication_model import UserAuthentication
from app.models.user_model import User
from app.models.user_profile_model import UserProfile
from app.utils.generate_expire_time import gen_exp_time
from app.utils.generate_code import generate_numeric_code
from app.utils.service.send_email import send_email
from fastapi import BackgroundTasks ,HTTPException
from app.enums.user_enum import AccountStatus,AuthenticationStatus ,AuthenticationType

from app.utils.password_hashed import hash_password ,verify_password
from app.utils.is_time_expire import is_time_expired
from datetime import timezone, datetime
from typing import Optional
from app.utils.jwt import create_access_refresh_tokens

from app.schemas.function_return_schema.create_access_refresh_token_schema import JwtPayload,AccessRefreshToken
from app.schemas.api_response_model.user_login import LoginResponse
from app.schemas.function_return_schema.user_repository_schema import VerifyResetPassResult
from app.schemas.api_response_model.user_signup import SignupResponse
from app.schemas.api_response_model.verify_user import VerifyUserResponse
class UserService:
    @staticmethod
    async def create_user_with_profile(
        db:AsyncSession,data:CreateUserWithProfile, background_tasks: BackgroundTasks
    )->SignupResponse:
      
      user_auth_data=await UserRepository.get_user_auth_data(db,data.email)

      if user_auth_data:

        if user_auth_data.is_verified:
          raise HTTPException(status_code=400, detail="You already have an account.")

        if user_auth_data.account_status==AccountStatus.pending or user_auth_data.is_verified==False :

          await UserRepository.delete_user(db,str(user_auth_data.id))


      user=User(email=data.email,password=hash_password(data.password))
      user=await UserRepository.create_user(db,user)

      profile_data=data.profile
      profile=UserProfile(user_id=user.id,**profile_data.model_dump())
      profile=await UserRepository.create_profile(db,profile)

      authentication=UserAuthentication(user_id=user.id,code=generate_numeric_code(4),expire_time= gen_exp_time(10) ,authentication_type=AuthenticationType.email )
      authentication=await UserRepository.create_new_authentication(db,authentication)
      await db.commit()
      await db.refresh(user)
   
     
      # Schedule email in the background
      background_tasks.add_task(
                send_email,
                "md.tazwarul.islam.07@gmail.com",
                "Testing email",
                "Test message"
            )
        
      response= SignupResponse(
          message= "A verification code has been sent to your email.",
          user_id= user.id
        )

      return response
    
    @staticmethod
    async def verifyUser(db: AsyncSession, user_id: str, code: Optional[str]=None,token:Optional[str]=None)->VerifyUserResponse:
      verify_data:Optional[VerifyResetPassResult]=None
      generated_token:Optional[AccessRefreshToken]=None
      user_data = await UserRepository.get_user_auth_data(db, user_id)
      user_last_verification_data = await UserRepository.get_latest_authentication(db, user_id)

      if not user_data:
        raise HTTPException(status_code=404, detail="Failed to verify")
      

      if not user_last_verification_data:
        raise HTTPException(status_code=404, detail="Failed to verify")
      
      if user_last_verification_data.authentication_status!=AuthenticationStatus.pending:
         raise HTTPException(status_code=400, detail="Code or Token not matched.")



      expire_time: Optional[datetime] = getattr(user_last_verification_data, "expire_time", None)

 
      if expire_time is None:
        raise HTTPException(status_code=400, detail="Expire time missing")

      if expire_time.tzinfo is None:
        expire_time = expire_time.replace(tzinfo=timezone.utc)
      else:
        expire_time = expire_time.astimezone(timezone.utc)

      expired = is_time_expired(expire_time)
      if expired:
        raise HTTPException(status_code=400, detail="Verification time expired") 
 
      if user_last_verification_data.code and user_last_verification_data.token is None:
        if user_last_verification_data.code!=code:
          raise HTTPException(status_code=400, detail="Code not matched.") 
        
      if not user_last_verification_data.code and user_last_verification_data.token:
         if user_last_verification_data.token !=token:
          raise HTTPException(status_code=400, detail="Token not matched") 


      if user_last_verification_data.authentication_type==AuthenticationType.email:
        await UserRepository.verifyUserEmail(db,user_id=user_id,user_authentication_id=str(user_last_verification_data.id))
        payload:JwtPayload={
          "user_id":user_id,
          "user_email":user_data.email,
          "user_role":user_data.role
        }
        generated_token=create_access_refresh_tokens(payload=dict(payload) )
  
   
      if user_last_verification_data.authentication_type==AuthenticationType.password:
        verify_data= await UserRepository.verifyResetPassword(db,user_id=user_id,user_authentication_id=str(user_last_verification_data.id))

      await db.commit()

      res=VerifyUserResponse(
      user_id=user_id,
      access_token= generated_token and generated_token["access_token"],
      refresh_token=generated_token and generated_token["refresh_token"],
      token= verify_data and verify_data["token"]
    )
      return  res


    @staticmethod
    async def userLogin(db:AsyncSession,user_email:str,password:str)-> LoginResponse:
      user_data=await UserRepository.get_user_auth_data(session=db,user_email=user_email)
      if not user_data: 
        raise HTTPException(status_code=404, detail="Account not found.") 
      if not verify_password(plain_password=password,hashed_password=user_data.password):
        raise HTTPException(status_code=400, detail="Password not matched") 
      if user_data.account_status!=AccountStatus.active:
        raise HTTPException(status_code=400, detail=f"Account status is {user_data.account_status.value}")
      
      payload:JwtPayload={
      "user_email":user_data.email,
      "user_id":str(user_data.id),
      "user_role":user_data.role
      }
      
      generated_token=create_access_refresh_tokens(payload=dict(payload))

      return LoginResponse(user_id=user_data.id, access_token=generated_token["access_token"], refresh_token=generated_token["refresh_token"])
    
    @staticmethod
    async def resendCode(db:AsyncSession,user_id:str,)->str:
      user_last_verification_data = await UserRepository.get_latest_authentication(db, user_id)
      if not user_last_verification_data:
        raise HTTPException(status_code=404,detail="Failed to send verification code.")
      
      await UserRepository.updateStatusOfVerification(db,str(user_last_verification_data.id),AuthenticationStatus.canceled)

      new_auth_data=UserAuthentication(authentication_type=user_last_verification_data.authentication_type,code=generate_numeric_code(4),expire_time=gen_exp_time(),user_id=user_last_verification_data.user_id)
      
      await UserRepository.create_new_authentication(session=db,data=new_auth_data)
      await db.commit()
      return user_id



