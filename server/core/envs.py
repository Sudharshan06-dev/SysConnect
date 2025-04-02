import os
from dotenv import load_dotenv
load_dotenv()

class Envs:
    AWS_ACCESS_KEY = "your_access_key"
    AWS_SECRET_KEY = "your_secret_key"
    AUTH_SECRET_KEY = os.getenv('SECRET_KEY')
    AUTH_ALGORITHM = os.getenv('ALGORITHM')
    AUTH_EXPIRATION = 30 * 60 * 60
    S3_REGION = "us-east-1"
    S3_BASE_URL = f"https://s3.{S3_REGION}.amazonaws.com"
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_SERVER = os.getenv('MAIL_SERVER')
