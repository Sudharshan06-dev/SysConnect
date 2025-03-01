from fastapi import APIRouter, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from core.context_vars import user_id_ctx
from core.auth import get_current_user
from core.database import get_db
from core.constants import RoleTypeWithAdmin
from admin.application import application_router

# Create a router for admin endpoints
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
    
admin_router.include_router(application_router)