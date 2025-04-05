from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from core.auth import get_hashed_password
from sqlalchemy.exc import SQLAlchemyError
from config.database import get_db
from core.models import UserModel, ApplicationModel
from core.constants import ApplicationStatus
from core.utility import create_response
from core.constants import SUCCESS, ERROR
from core.schemas import ApplicationResponse, CreateApplicationUserRequest
import random
import string
import logging

logger = logging.getLogger(__name__)

registration_router = APIRouter(prefix='/register')

"""Generate a random alphanumeric reference number."""
def generate_reference_number(length=10):
    characters = string.ascii_uppercase + string.digits  # A-Z, 0-9
    return ''.join(random.choices(characters, k=length))

@registration_router.post("/register-user", response_model=ApplicationResponse)
async def create_application_user(user_data: CreateApplicationUserRequest, db: Session = Depends(get_db)):

    try:

        hashed_password = get_hashed_password(user_data.password)

        # Create user in the main database
        db_user = UserModel(
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            role=user_data.role
        )

        db.add(db_user)
        db.commit()  # Commit to generate user_id
        db.refresh(db_user)  # Refresh to get the generated ID

        # Create application and associate with the user
        db_application_user = ApplicationModel(
            user_id = db_user.user_id,
            reference_number = generate_reference_number(),
            degree = user_data.degree if user_data.degree else None,
            major = user_data.major if user_data.major else None,
            role = user_data.role,
            application_status = ApplicationStatus.PENDING
        )

        db.add(db_application_user)
        db.commit()
        db.refresh(db_application_user)

        return create_response(200, "register_user", SUCCESS)

    except SQLAlchemyError:
        db.rollback()
        logger.exception("Database error in creating user")
        return create_response(500, "invalid_user", ERROR)

    except Exception:
        logger.exception("Unexpected error in creating user")
        return create_response(500, "invalid_user", ERROR)