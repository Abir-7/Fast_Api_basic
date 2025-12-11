import os
from dotenv import load_dotenv

# Load .env once
load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME") # type: ignore
    APP_ENV: str = os.getenv("APP_ENV") # type: ignore
    # email
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    EMAIL_USER: str = os.getenv("EMAIL_USER") # type: ignore
    EMAIL_PASS: str = os.getenv("EMAIL_PASS") # type: ignore
    # data base
    DATABASE_URL: str = os.getenv("DATABASE_URL") # type: ignore
    ACCESS_TOKEN_SECRET:str=os.getenv("ACCESS_TOKEN_SECRET") # type: ignore
    REFRESH_TOKEN_SECRET:str=os.getenv("REFRESH_TOKEN_SECRET") # type: ignore

    
settings = Settings()
