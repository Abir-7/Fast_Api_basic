from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.user_model import User
from app.models.user_profile_model import UserProfile
from app.models.user_authentication_model import UserAuthentication
from app.enums.user_enum import AuthenticationStatus,AuthenticationType ,AccountStatus
from sqlmodel import select ,desc
from app.utils.create_random_token import create_random_token
from app.utils.generate_expire_time import gen_exp_time
from typing import Optional
from app.schemas.function_return_schema.user_repository_schema import VerifyUserEmailResult,VerifyResetPassResult
from uuid import UUID
from app.schemas.user_schema import UserUpdate
from app.utils.password_hashed import hash_password
class UserRepository:
    @staticmethod
    async def get_user_auth_data(session:AsyncSession,user_email:Optional[str]=None,user_id:Optional[str]=None):

        if not user_email and not user_id:
            return None
        
        query=select(User)

        if user_email:
            query.where(User.email==user_email)
        if user_id:
            query.where(User.id==user_id)

        result= await session.exec(query)
        user=result.one_or_none()

        return user

    @staticmethod
    async def create_user(session:AsyncSession,user:User):
        session.add(user)
        await session.flush()
        return user

    @staticmethod
    async def create_profile(session:AsyncSession,user_profile:UserProfile):
        session.add(user_profile)
        await session.flush()
        return user_profile
    
    @staticmethod
    async def create_new_authentication(session:AsyncSession,data:UserAuthentication):
        session.add(data)
        await session.flush()
        return data
    
    @staticmethod
    async def delete_user(session:AsyncSession,user_id:str):
        result= await session.exec(select(User).where(User.id ==user_id))
        user=result.one_or_none()
        if not user:
            return None
        await session.delete(user)
        await session.flush()
        return user
    
    @staticmethod
    async def get_latest_authentication(session: AsyncSession, user_id: str) -> UserAuthentication | None:

        result = await session.exec(
            select(UserAuthentication)
            .where(UserAuthentication.user_id == user_id)
            .order_by(desc(UserAuthentication.created_at))  # assuming you have a 
            .limit(1)
        )
        return result.one_or_none()
    
    @staticmethod
    async def verifyResetPassword(session:AsyncSession,user_id:str,user_authentication_id:str)->VerifyResetPassResult:
        auth_data=await session.exec(select(UserAuthentication).where(UserAuthentication.id==user_authentication_id))
        auth_data_result=auth_data.one_or_none()

        auth_data_result.authentication_status=AuthenticationStatus.success # type: ignore
 

        user_data=await session.exec(select(User).where(User.id==user_id))
        user_data_result= user_data.one_or_none()
        user_data_result.need_to_reset_password=True # type: ignore

        
        new_token= create_random_token()
        new_auth=UserAuthentication(authentication_type=AuthenticationType.password,user_id=UUID(user_id),token=new_token,expire_time=gen_exp_time())
        session.add(new_auth)

        session.add(user_data_result)
        session.add( auth_data_result)
        await session.flush()

        return {"token":new_token,"user_id":user_id}
    
    @staticmethod
    async def verifyUserEmail(session:AsyncSession,user_id:str ,user_authentication_id:str)->VerifyUserEmailResult:

        auth_data=await session.exec(select(UserAuthentication).where(UserAuthentication.id==user_authentication_id))
        auth_data_result=auth_data.one_or_none()
        auth_data_result.authentication_status=AuthenticationStatus.success # type: ignore
        session.add(auth_data_result)

        user_data=await session.exec(select(User).where(User.id==user_id))
        user_data_result= user_data.one_or_none()
        if user_data_result:
            user_data_result.is_verified=True 
            user_data_result.account_status=AccountStatus.active
        session.add(user_data_result)

        await session.flush()
        
        return {"user_id":user_id}
    
    @staticmethod
    async def updateStatusOfVerification(session:AsyncSession,authentication_id:str,status:AuthenticationStatus)->str:
        auth_data=await session.exec(select(UserAuthentication).where(UserAuthentication.id==authentication_id))
        auth_data_result=auth_data.one_or_none()
        if auth_data_result  :      
         auth_data_result.authentication_status=status
         session.add(auth_data_result)
        await session.flush()
        return status
    
    @staticmethod
    async def updateUser(session:AsyncSession,user_id:str,data:UserUpdate
    ):
        user=await session.exec(select(User).where(User.id==user_id))
        user=user.one_or_none()

        if not user:
            raise ValueError("User not found")
        
        update_data = data.model_dump(exclude_unset=True)

        if "password" in update_data:
            user.password = hash_password(update_data.pop("password"))

        for field, value in update_data.items():
         setattr(user, field, value)
        
        session.add(user)
        await session.flush()