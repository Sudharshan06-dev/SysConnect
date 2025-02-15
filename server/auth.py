from fastapi import HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from models import UserModel
from typing import Optional
from constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import UserResponse
import jwt

#Add all the contexts and dependecies need to be used
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

#First time entry to the user table => password needs to be hashed
def get_hashed_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

#User Logs in => Check the hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user_details(username: str, db: Session) -> Optional[UserModel]:
    return db.query(UserModel).filter(UserModel.username == username).first()

def authenticate_user(username: str, password: str, db: Session) -> Optional[UserModel]:
    user = get_user_details(username, db)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserResponse:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="User not found")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="User not found")

    user = get_user_details(username, db)

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return UserResponse.model_validate(user)