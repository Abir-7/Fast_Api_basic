import os
from dotenv import load_dotenv

# Load .env once
load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME")
    APP_ENV: str = os.getenv("APP_ENV")
    # email
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    EMAIL_USER: str = os.getenv("EMAIL_USER")
    EMAIL_PASS: str = os.getenv("EMAIL_PASS")
    # data base
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    ACCESS_TOKEN_SECRET:str=os.getenv("ACCESS_TOKEN_SECRET")
    REFRESH_TOKEN_SECRET:str=os.getenv("REFRESH_TOKEN_SECRET")

    
settings = Settings()
