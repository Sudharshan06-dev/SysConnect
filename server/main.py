from fastapi import FastAPI, HTTPException, Depends,status, Response
from config.database import engine, get_db
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from core.models import UserTokenModel, Base
from core.auth import authenticate_user, create_access_token, oauth2_scheme
from core.schemas import UserResponse, UserLoginResponse, DefaultResponse
from core.user_middleware import user_middleware
from login import router as login_router
from admin import admin_router, AdminMiddleware as admin_middleware
from core.context_vars import user_id_ctx

#Instantiate the fastapi app
app = FastAPI()

routers = [login_router, admin_router]
middlewares = [user_middleware, admin_middleware]

# Custom Middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=user_middleware)
#app.add_middleware(admin_middleware)

#Add all the routes for the application
for app_router in routers:
    app.include_router(app_router)


#Spin up all the models that is needed to be created
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.post("/token", response_model= UserLoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})

    update_user_token = UserTokenModel(
        user_id = user.user_id,
        user_token=access_token
    )

    db.add(update_user_token)
    db.commit()
    db.refresh(update_user_token)

    return UserLoginResponse(access_token=access_token, user=user)

@app.post("/logout", response_model=DefaultResponse)
async def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    token_entry = await db.query(UserTokenModel).filter(UserTokenModel.user_token == token.access_token and UserTokenModel.user_id == user_id_ctx.get('user_id')).first()

    if token_entry:
        token_entry.is_revoked = True
    
    db.commit()

    return DefaultResponse(title="Success", message="Successfully logged out and token revoked")

