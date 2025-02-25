from fastapi import Request
from sqlalchemy.orm import Session
from constants import SECRET_KEY, ALGORITHM
from auth import get_db, get_current_user  # Import your auth functions
from context_vars import user_id_ctx
import jwt

#Authorization
async def my_middleware(request: Request, call_next):
        
    auth_header = request.headers.get("Authorization")
    
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
