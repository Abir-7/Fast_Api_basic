from enum import Enum

class UserRole(str, Enum):
    USER = "USER"
    SUPER_ADMIN = "SUPER_ADMIN"

class AccountStatus(str, Enum):
    pending = "pending"
    active = "active"
    deleted= "deleted"
    blocked= "blocked"

class AuthenticationStatus(str, Enum):
    pending =   "pending"
    expired =   "expired"
    canceled =  "canceled"
    success =   "success"   

class AuthenticationType(str,Enum):
    email="email"
    password="password"