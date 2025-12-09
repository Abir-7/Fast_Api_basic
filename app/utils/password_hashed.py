from pwdlib import PasswordHash


# Create a Password instance using Argon2
pwd_context = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Hash plain text password using Argon2.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify plain password against hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)
