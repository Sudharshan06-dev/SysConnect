from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.orm import Session
from auth import get_hashed_password, get_current_user
from database import get_db
from context_vars import user_id_ctx
from models import UserModel
from schemas import UserResponse, CreateUserRequest

router = APIRouter(prefix='/user')

@router.post("/create-user", response_model=UserResponse)
async def create_user(user_data: CreateUserRequest, db: Session = Depends(get_db)):

    hashed_password = get_hashed_password(user_data.password)

    db_user = UserModel(
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        role=user_data.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse.model_validate(db_user)


@router.get("/current-user", response_model=UserResponse)
async def get_current_user_route(current_user: UserResponse = Depends(get_current_user)):
    return user_id_ctx.get()