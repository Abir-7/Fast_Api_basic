import aiosmtplib
from email.message import EmailMessage
from app.core.config import settings  # your Settings class

async def send_email(to: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = settings.EMAIL_USER
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_SERVER,
        port=settings.SMTP_PORT,
        start_tls=True,
        username=settings.EMAIL_USER,
        password=settings.EMAIL_PASS,
    )
