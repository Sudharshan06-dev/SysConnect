from fastapi import APIRouter, Depends, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from core.context_vars import user_id_ctx
from core.auth import get_current_user
from config.database import get_db
from core.constants import RoleType

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

async def admin_middleware(request: Request, db: Session = Depends(get_db)):

    if user_id_ctx.get() is None:
        current_user = await get_current_user(request, db)
        user_id_ctx.set(current_user)


    if getattr(user_id_ctx.get(), "role", None) != RoleType.ADMIN:
        raise HTTPException(status_code=403, detail="Forbidden: Admins only")