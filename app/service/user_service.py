from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.user_schema import CreateUserWithProfile
from app.repository.user_repository import UserRepository
from app.models.user_authentication_model import UserAuthentication
from app.models.user_model import User
from app.models.user_profile_model import UserProfile
from app.utils.generate_expire_time import gen_exp_time
from app.utils.generate_code import generate_numeric_code
from app.utils.service.send_email import send_email
from fastapi import BackgroundTasks
from app.enums.user_enum import AccountStatus
from fastapi import HTTPException 
from fastapi.responses import JSONResponse 
from app.utils.password_hashed import hash_password
from app.utils.is_time_expire import is_time_expired
from datetime import timezone, datetime
class UserService:
    @staticmethod
    async def create_user_with_profile(
        db:AsyncSession,data:CreateUserWithProfile, background_tasks: BackgroundTasks
    ):
      
      user_auth_data=await UserRepository.get_user_auth_data(db,data.email)

      if user_auth_data:

        if user_auth_data.is_verified:
          return JSONResponse(status_code=400 ,content={"message":"You already have a account."})
          # raise  HTTPException(status_code=400,detail="You already have a account.")


        if user_auth_data.account_status==AccountStatus.pending or user_auth_data.is_verified==False :

          await UserRepository.delete_user(db,user_auth_data.id)


      user=User(email=data.email,password=hash_password(data.password))
      user=await UserRepository.create_user(db,user)

      profile_data=data.profile
      profile=UserProfile(user_id=user.id,**profile_data.model_dump())
      profile=await UserRepository.create_profile(db,profile)

      authentication=UserAuthentication(user_id=user.id,code=generate_numeric_code(4),expire_time= gen_exp_time(10) )
      authentication=await UserRepository.create_new_authentication(db,authentication)
      await db.commit()
      await db.refresh(user)
      db.close()
     
        # Schedule email in the background
      # background_tasks.add_task(
      #           send_email,
      #           "md.tazwarul.islam.07@gmail.com",
      #           "Testing email",
      #           "Test message"
      #       )
        
      return {"user_id":user.id,"message":"A verification code has been sent to your email."}
    
    @staticmethod
    async def verifyUser(db:AsyncSession,user_id:str,code:str):
    
      user_authentication_data=await UserRepository.get_user_auth_data(db,user_id)
      user_last_verification_data=await UserRepository.get_latest_authentication(db,user_id)

      if not user_authentication_data:
        return JSONResponse(status_code=404,content={"message":"No data found"})
      expire_time = user_last_verification_data.expire_time
    # Force UTC-aware for consistent output
      if expire_time.tzinfo is None:
        expire_time = expire_time.replace(tzinfo=timezone.utc)

      return {
          "isExpired": is_time_expired(expire_time),
        "exptime": expire_time.isoformat() 
          # returns "2025-12-09T09:38:52.494253+00:00"
          ,"now":datetime.now(timezone.utc)
    }
      