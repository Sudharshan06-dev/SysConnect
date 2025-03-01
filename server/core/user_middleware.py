from fastapi import Request
from sqlalchemy.orm import Session
from core.envs import Envs
from core.auth import get_db, get_current_user  # Import your auth functions
from core.context_vars import user_id_ctx
import jwt

#Authorization
async def user_middleware(request: Request, call_next):
        
    auth_header = request.headers.get("Authorization")
    
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, Envs.AUTH_SECRET_KEY, algorithms=[Envs.AUTH_ALGORITHM])
            username = payload.get("sub")
            
            if username:
                db: Session = next(get_db())  
                user = await get_current_user(token, db)
                user_id_ctx.set(user)
    
        except Exception as e:
            print('e', e)
            pass
    
    response = await call_next(request)

    return response
