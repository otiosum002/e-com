from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr

class EmailConfig:
    MAIL_USERNAME = "email"
    MAIL_PASSWORD = " "
    MAIL_FROM = "email"
    MAIL_PORT = 587
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_FROM_NAME = "E-commerce App"

mail_config = ConnectionConfig(
    MAIL_USERNAME=EmailConfig.MAIL_USERNAME,
    MAIL_PASSWORD=EmailConfig.MAIL_PASSWORD,
    MAIL_FROM=EmailConfig.MAIL_FROM,
    MAIL_PORT=EmailConfig.MAIL_PORT,
    MAIL_SERVER=EmailConfig.MAIL_SERVER,
    MAIL_FROM_NAME=EmailConfig.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

mail = FastMail(mail_config)

async def send_verification_email(email: EmailStr, username: str, verification_url: str):
    html = f"<p>Hi {username},</p><p>Click <a href='{verification_url}'>here</a> to verify your email.</p>"
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )
    await mail.send_message(message) 