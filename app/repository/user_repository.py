from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.user_model import User
from app.models.user_profile_model import UserProfile
from app.models.user_authentication_model import UserAuthentication
from sqlmodel import select ,desc
class UserRepository:
    @staticmethod
    async def get_user_auth_data(session:AsyncSession,user_email:str):
        result= await session.exec(select(User).where(User.email ==user_email))
        user=result.one_or_none()
        if not user:
            return None
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