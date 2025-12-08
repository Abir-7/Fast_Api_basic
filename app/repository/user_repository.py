from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.user_model import User
from app.models.user_profile_model import UserProfile
from app.models.user_authentication_model import UserAuthentication
class UserRepository:
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
    async def craete_new_authentication(session:AsyncSession,data:UserAuthentication):
        session.add(data)
        await session.flush()
        return data