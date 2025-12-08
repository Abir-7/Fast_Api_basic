from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    SUPER_ADMIN = "super_admin"

class AuthenticationStatus(str, Enum):
    PENDING = "pending"
    EXPIRED = "expired"
    CANCELED = "canceled"
    SUCCESS = "success"