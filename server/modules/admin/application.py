from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import List
from core.schemas import ApproveRequest, BulkApproveRequest, ApplicationResponse
from config.database import get_db
from core.auth import get_current_user
from core.constants import ApplicationStatus, RoleType, SUCCESS, ERROR
from core.models import ApplicationModel, UserModel
from core.email_sender import sendEmail
from core.utility import create_response
from modules.admin import admin_routing_middleware as admin_middleware 
import logging
import asyncio

logger = logging.getLogger(__name__)

#Schedule based on professors, courses. Courses should not overlap for the professors, 

application_router = APIRouter(prefix='/application')

#APPROVE A SINGLE USER
@application_router.put('/{user_type}/{application_id}/approve', response_class=JSONResponse, dependencies=[Depends(admin_middleware)])
async def approve_user(
    user_type: str,
    application_id: int,
    user_data: ApproveRequest,
    _ = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Approve a single user application.
    """
    try:
        email_sent = await sendEmail(user_data.email)

        if email_sent:
            application_data = await _update_application_status(user_type, application_id, ApplicationStatus.APPROVED, db)

            if not application_data:
                return create_response(422, "approve_user", ERROR)

            await _update_user_role(application_data.user_id, application_data.role, db)
            return create_response(200, "approve_user", SUCCESS)
        
        return create_response(422, "approve_user", ERROR)

    except Exception as e:
        logger.error(f"Error in approve_user for {user_type} ID {application_id}: {str(e)}")
        return create_response(500, "approve_user", ERROR)


#REJECT A SINGLE USER
@application_router.put('/{user_type}/{application_id}/reject', response_class=JSONResponse, dependencies=[Depends(admin_middleware)])
async def reject_user(
    user_type: str,
    application_id: int,
    user_data: ApproveRequest,
    _ = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Reject a single user application.
    """
    try:
        email_sent = await sendEmail(user_data.email)

        if email_sent:
            application_data = await _update_application_status(user_type, application_id, ApplicationStatus.REJECTED, db)

            if not application_data:
                return create_response(422, "approve_user", ERROR)
            
            _update_user_role(application_data.user_id, application_data.role, db)
                
            return create_response(200, "reject_user", SUCCESS)

        return create_response(422, "reject_user", ERROR)

    except Exception as e:
        logger.error(f"Error in reject_user for {user_type} ID {application_id}: {str(e)}")
        return create_response(500, "reject_user", ERROR)


#APPROVE MULTIPLE USERS
@application_router.put('/{user_type}/approve', response_class=JSONResponse, dependencies=[Depends(admin_middleware)])
async def approve_multiple_users(
    user_type: str,
    users_data: List[BulkApproveRequest],
    _ = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Approve multiple users in bulk.
    """
    try:
        email_list = [user.email for user in users_data]

        # Fire & forget - Emails are sent in the background
        asyncio.create_task(send_bulk_email(email_list))

        # Process DB updates without waiting for emails
        for user in users_data:
            application_data = await _update_application_status(user_type, user.application_id, ApplicationStatus.APPROVED, db)

            if not application_data:
                return create_response(422, "approve_user", ERROR)

            _update_user_role(application_data.user_id, application_data.role, db)

        return create_response(200, "multiple_user")

    except Exception as e:
        logger.error(f"Error in approve_multiple_users for {user_type}: {str(e)}")
        return create_response(500, "multiple_user", ERROR)


#REJECT MULTIPLE USERS
@application_router.put('/{user_type}/reject', response_class=JSONResponse, dependencies=[Depends(admin_middleware)])
async def reject_multiple_users(
    user_type: str,
    users_data: List[BulkApproveRequest],
    _ = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Reject multiple user applications in bulk.
    """
    try:
        email_list = [user.email for user in users_data]

        # Fire & forget - Emails are sent in the background
        asyncio.create_task(send_bulk_email(email_list))

        # Process DB updates without waiting for emails
        for user in users_data:
            application_data = await _update_application_status(user_type, user.application_id, ApplicationStatus.REJECTED, db)

            if not application_data:
                return create_response(422, "approve_user", ERROR)

            _update_user_role(application_data.user_id, application_data.role, db)

        return create_response(200, "reject_multiple_users")

    except Exception as e:
        logger.error(f"Error in reject_multiple_users for {user_type}: {str(e)}")
        return create_response(500, "reject_multiple_users", ERROR)


#GET ALL PENDING USERS
@application_router.get('/{user_type}/all', response_model=List[ApplicationResponse], dependencies=[Depends(admin_middleware)])
async def get_pending_users(
    user_type: str,
    db: Session = Depends(get_db),
    _ = Depends(get_current_user),
):
    """
    Fetch all pending applications for a given user type.
    """
    try:
        pending_users = db.query(ApplicationModel).filter(
            (ApplicationModel.application_status == ApplicationStatus.PENDING) &
            (ApplicationModel.role == user_type)
        ).all()

        return ApplicationResponse.model_validate(pending_users, from_attributes=True)

    except Exception as e:
        logger.error(f"Error in get_pending_users for {user_type}: {str(e)}")
        return []


#FETCH DETAILS ABOUT A SPECIFIC APPLICATION
@application_router.get('/{user_type}/application/{application_id}', response_model=ApplicationResponse, dependencies=[Depends(admin_middleware)])
async def get_application_details(
    user_type: str,
    application_id: int,
    db: Session = Depends(get_db),
    _ = Depends(get_current_user),
):
    """
    Fetch details of a specific application.
    """
    try:
        application_data = db.query(ApplicationModel).filter(
            (ApplicationModel.role == user_type) &
            (ApplicationModel.application_id == application_id)
        ).first()

        if application_data:
            return ApplicationResponse.model_validate(application_data)

        return create_response(422, "get_specific_application", ERROR)

    except Exception as e:
        logger.error(f"Error in get_application_details for {user_type} ID {application_id}: {str(e)}")
        return create_response(500, "get_specific_application", ERROR)


'''
INTERNAL HELPERS STARTS
'''
##INTERNAL HELPERS ##
async def _update_application_status(user_type: str, application_id: int, status: ApplicationStatus, db: Session):

    application = db.query(ApplicationModel).filter(
        (ApplicationModel.role == user_type) &
        (ApplicationModel.application_id == application_id)
    ).first()

    if application:
        application.application_status = status
        db.commit()
        return application
    
    return None


async def send_bulk_email(email_list):
    for email in email_list:
        await sendEmail(email)  # Ensure `sendEmail` is async

async def _update_user_role(user_id: int, user_role_status: RoleType, db: Session):

    try:

        user_data = db.query(UserModel).filter(UserModel.user_id == user_id).first()

        if user_data:
            user_data.role = user_role_status
            db.commit()
            return user_data
        
        return None

    except Exception as e:
        db.rollback()
        logger.error(f"Error in _create_user: {str(e)}")
'''
INTERNAL HELPERS ENDS
'''