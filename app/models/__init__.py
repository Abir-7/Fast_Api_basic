from .user_model import User
from .user_profile_model import UserProfile
from .user_authentication_model import UserAuthentication
from sqlmodel import SQLModel

# Optional: expose metadata for Alembic
metadata = SQLModel.metadata

# Tell linters / IDEs these are intentionally exported
__all__ = [
    "User",
    "UserProfile",
    "UserAuthentication",
    "metadata",
]
