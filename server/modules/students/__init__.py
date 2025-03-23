from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from core.auth import get_db, get_current_user
from core.context_vars import user_id_ctx
from core.schemas import RoleType

applicant_router = APIRouter(prefix="/student", tags=["Student"])


async def student_middleware(request: Request, db: Session = Depends(get_db)):
    if user_id_ctx.get() is None:
        current_user = await get_current_user(request, db)
        user_id_ctx.set(current_user)

    if user_id_ctx.get('role') not in {RoleType.STUDENT, RoleType.ADMIN}:
        raise HTTPException(status_code=403, detail="Forbidden: Students only")