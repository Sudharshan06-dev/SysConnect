from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from core.auth import get_hashed_password, get_current_user
from core.database import get_db
from uuid import uuid4
from core.context_vars import user_id_ctx
from core.models import UserModel, ApplicationModel
from core.constants import ApplicationStatus
from core.schemas import ApplicationResponse, UserResponse, CreateUserRequest

router = APIRouter(prefix='/user')

@router.post("/create-application-user", response_model=ApplicationResponse)
async def create_application_user(user_data: CreateUserRequest, db: Session = Depends(get_db)):

    hashed_password = get_hashed_password(user_data.password)

    #Create application and change the response
    db_application_user =  ApplicationModel(
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        email=user_data.email,
        username=user_data.username,
        #reference_number=uuid4(),
        #application_status=ApplicationStatus.PENDING,
        hashed_password=hashed_password,
        role=user_data.role
    )

    db.add(db_application_user)
    db.commit()
    db.refresh(db_application_user)

    return ApplicationResponse.model_validate(db_application_user)


@router.get("/current-user", response_model=UserResponse)
async def get_current_user_route(_: UserResponse = Depends(get_current_user)):
    return user_id_ctx.get()