from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.request.auth_request_schema import CreateUserWithProfile ,ResetPassword
from app.schemas.request.user_request_schema import UpdateUser
from app.repository.user_repository import UserRepository
from app.models.user_authentication_model import UserAuthentication
from app.models.user_model import User
from app.models.user_profile_model import UserProfile
from app.utils.generate_expire_time import gen_exp_time
from app.utils.generate_code import generate_numeric_code
from app.utils.send_email import send_email
from fastapi import BackgroundTasks ,HTTPException
from app.enums.user_enum import AccountStatus,AuthenticationStatus ,AuthenticationType

from app.utils.password_hashed import hash_password ,verify_password


from app.utils.is_time_expire import is_time_expired
from datetime import timezone, datetime
from typing import Optional,Union
from uuid import UUID
from app.utils.jwt import create_access_refresh_tokens, create_token ,decode_token,TokenType

from app.schemas.internal.jwt_token_schema import JwtPayload,AccessRefreshToken
from app.schemas.response.auth_response_schema import LoginResponse

from app.schemas.response.auth_response_schema import SignupResponse 
from app.schemas.response.auth_response_schema import VerifyUserEmailResponse, VerifyUserResetPasswordResponse ,UserIdResponse,NewAccessTokenResponse




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
                data.email,
                "Testing email",
                "Test message"
            )
        
      response= SignupResponse(
          message= "A verification code has been sent to your email.",
          user_id= user.id
        )

      return response
    
    @staticmethod
    async def verifyUser(db: AsyncSession, user_id: str, code: Optional[str]=None,token:Optional[str]=None)->Union[VerifyUserResetPasswordResponse,VerifyUserEmailResponse]:
      verify_data:Optional[VerifyUserResetPasswordResponse]=None
      generated_token:Optional[AccessRefreshToken]=None
      user_data = await UserRepository.get_user_auth_data(db, user_id)
      user_last_verification_data = await UserRepository.get_latest_authentication(db, user_id)

      if not user_data:
        raise HTTPException(status_code=404, detail="Failed to verify")
      

      if not user_last_verification_data:
        raise HTTPException(status_code=404, detail="Failed to verify")
      
      if user_last_verification_data.authentication_status!=AuthenticationStatus.pending:
         raise HTTPException(status_code=400, detail="No invalid code found for resend.")


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



      res:Optional[Union[VerifyUserResetPasswordResponse, VerifyUserEmailResponse]] = None

      if user_last_verification_data.authentication_type==AuthenticationType.email:
        await UserRepository.verifyUserEmail(db,user_id=user_id,user_authentication_id=str(user_last_verification_data.id))
        payload:JwtPayload={
          "user_id":user_id,
          "user_email":user_data.email,
          "user_role":user_data.role
        }
        generated_token=create_access_refresh_tokens(payload=dict(payload) )
        res=VerifyUserEmailResponse(access_token=generated_token["access_token"],refresh_token=generated_token["refresh_token"],user_id=UUID(user_id))
  
   
      if user_last_verification_data.authentication_type==AuthenticationType.password:
        verify_data= await UserRepository.verifyResetPassword(db,user_id=user_id,user_authentication_id=str(user_last_verification_data.id))      
        res=VerifyUserResetPasswordResponse(token=verify_data.token,user_id=UUID(user_id))

      if res is None:
        raise HTTPException(status_code=400, detail="Failed to verify.") 

      await db.commit()
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
    async def resendCode(db:AsyncSession,user_id:str,)->UserIdResponse:
      user_last_verification_data = await UserRepository.get_latest_authentication(db, user_id)
      if not user_last_verification_data:
        raise HTTPException(status_code=404,detail="Failed to send verification code.")
      print("acb")
      await UserRepository.updateStatusOfVerification(db,str(user_last_verification_data.id),AuthenticationStatus.canceled)

      new_auth_data=UserAuthentication(authentication_type=user_last_verification_data.authentication_type,code=generate_numeric_code(4),expire_time=gen_exp_time(),user_id=user_last_verification_data.user_id)
      
      await UserRepository.create_new_authentication(session=db,data=new_auth_data)
      await db.commit()
      res=UserIdResponse(user_id=UUID(user_id))
      return res
    
    @staticmethod
    async def forgotPasswordRequest(db:AsyncSession,user_email:str,background_tasks:BackgroundTasks)->UserIdResponse:
      user_data=await UserRepository.get_user_auth_data(db,user_email=user_email)
      if not user_data:
        raise HTTPException(status_code=404,detail="Account not found.")
      new= UserAuthentication(authentication_type=AuthenticationType.password,code=generate_numeric_code(4),expire_time=gen_exp_time(),user_id=user_data.id)
      await UserRepository.create_new_authentication(data=new,session=db)
      await db.commit()

      background_tasks.add_task(
                send_email,
                user_email,
                "Testing email",
                "Test message"
            )
      
      res=UserIdResponse(user_id=user_data.id)
      return res
    @staticmethod 

    async def resetPassword(db:AsyncSession,data:ResetPassword):
      users_new_auth=await UserRepository.get_latest_authentication(db,str(data.user_id))
      if not users_new_auth:
        raise HTTPException(status_code=404,detail="No Data Found.")

      if is_time_expired(users_new_auth.expire_time):
        raise HTTPException(status_code=400,detail="Password change time expired.")
      
      if data.new_password !=data.confirm_password:
        raise HTTPException(status_code=400,detail="Password not matched")
      

      await UserRepository.updateStatusOfVerification(db,str(users_new_auth.id),AuthenticationStatus.success)

      update=UpdateUser(password=data.new_password,need_to_reset_password=False)
      await UserRepository.updateUser(db,user_id=str(data.user_id),data=update)
      await db.commit()

      return {"message":"Password reset successfully."}
    
    @staticmethod
    def getNewAccessToken(refresh_token:str)->NewAccessTokenResponse:
        decoded_data=decode_token(refresh_token,TokenType.REFRESH)
        
        if decoded_data is None:
          raise HTTPException(status_code=401,detail="Invalid refresh token")
        
        new_payload:JwtPayload={
          "user_email":decoded_data["user_email"],
          "user_id":decoded_data["user_id"],
          "user_role":decoded_data["user_role"]
        }

        access_token=  create_token(dict(new_payload),token_type=TokenType.ACCESS)
        res=NewAccessTokenResponse(access_token=access_token)
        return res

       




