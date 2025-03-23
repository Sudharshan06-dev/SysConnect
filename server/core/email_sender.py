from fastapi import BackgroundTasks
from core.envs import Envs
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

email_body = "This is an email from FASTAPI Test"

email_config = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_STARTTLS=True,  # Corrected field
    MAIL_SSL_TLS=False   # Corrected field
)

async def sendEmail(email: str):

    try:

        message = MessageSchema(
            subject="Check subject",
            recipients=[email],
            body="Test",
            subtype='html'
        )

        fm = FastMail(email_config)
        await fm.send_message(message)  # Directly await the email send task
        
    except Exception as e:
        print('Error occured while sending email ' + email, e)
        return False

    return True