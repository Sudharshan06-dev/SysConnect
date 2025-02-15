from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from constants import SECRET_KEY, ALGORITHM
from auth import get_db, get_current_user  # Import your auth functions
import jwt

#Authorization
class UserMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        user_id = 1
        auth_header = request.headers.get("Authorization")
        
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                username = payload.get("sub")

                if username:
                    db: Session = next(get_db())  
                    user = get_current_user(token, db)
                    user_id = user.user_id  # Extract user ID

            except Exception:
                pass
        
        response = await call_next(request)
        return response
