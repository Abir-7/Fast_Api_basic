from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.user_schema import CreateUserWithProfile
from app.repository.user_repository import UserRepository
from app.models.user_authentication_model import UserAuthentication
from app.models.user_model import User
from app.models.user_profile_model import UserProfile
from app.utils.generate_expire_time import gen_exp_time
from app.utils.service.send_email import send_email
from fastapi import BackgroundTasks

class UserService:
    @staticmethod
    async def create_user_with_profile(
        db:AsyncSession,data:CreateUserWithProfile, background_tasks: BackgroundTasks
    ):
      async with db.begin():     
        user=User(email=data.email,password=data.password)
        user=await UserRepository.create_user(db,user)

        profile_data=data.profile
        profile=UserProfile(user_id=user.id,**profile_data.model_dump())
        profile=await UserRepository.create_profile(db,profile)

        authentication=UserAuthentication(user_id=user.id,code="0000",expire_time= gen_exp_time(10) )
        authentication=await UserRepository.craete_new_authentication(db,authentication)
        
        db.refresh(user)

     
        # Schedule email in the background
        background_tasks.add_task(
                send_email,
                "md.tazwarul.islam.07@gmail.com",
                "Testing email",
                "Test message"
            )
        
        return {"user_id":user.id,"message":"A verification code has been sent to your email."}