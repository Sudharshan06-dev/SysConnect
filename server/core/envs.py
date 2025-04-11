import os
from dotenv import load_dotenv
load_dotenv()

class Envs:
    AUTH_SECRET_KEY = os.getenv('SECRET_KEY')
    AUTH_ALGORITHM = os.getenv('ALGORITHM')
    AUTH_EXPIRATION = 30 * 60 * 60
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_SERVER = os.getenv('MAIL_SERVER')

    print(f"Envs.AUTH_ALGORITHM inside Envs Class: {AUTH_ALGORITHM}") #Add this line.
