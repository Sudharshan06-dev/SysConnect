from fastapi import APIRouter, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from core.context_vars import user_id_ctx
from core.auth import get_current_user
from config.database import get_db
from core.constants import RoleTypeWithAdmin
from admin.application import application_router
from admin.courses.course_service import course_router

# Create a router for admin endpoints
routers = [application_router, course_router]

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

class AdminMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        if user_id_ctx.get() is None:
            db: Session = next(get_db())  # Get the DB session
            current_user = await get_current_user(request, db)  # Get the authenticated user
            user_id_ctx.set(current_user)
        
        if user_id_ctx.get('role') != RoleTypeWithAdmin.ADMIN:
            raise HTTPException(status_code=403, detail="Forbidden: Admins only")

        response = await call_next(request)
        return response

for admin_routers in routers:
    admin_router.include_router(admin_routers)