from fastapi import FastAPI, HTTPException, Depends,status, Response
from fastapi.middleware.cors import CORSMiddleware
from config.database import engine, get_db
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from core.models import UserTokenModel, Base
from core.auth import authenticate_user, create_access_token, oauth2_scheme
from core.schemas import UserLoginResponse, DefaultResponse, UserResponse, UserLoginRequest
from core.user_middleware import user_middleware
from core.auth import get_current_user
from modules.admin import admin_router
from core.context_vars import user_id_ctx
from modules.admin.application import application_router as admin_application_router
from modules.admin.courses.course_service import course_router as admin_course_router
from registration import registration_router

#Instantiate the fastapi app
app = FastAPI()

#Adding all the necessary routes before adding it to the main router
admin_featured_routers = [admin_application_router, admin_course_router]

for admin_feature_router in admin_featured_routers:
    admin_router.include_router(admin_feature_router)


routers = [registration_router, admin_router]

origins = [
    "http://localhost:4200",
]

# Custom Middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=user_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Add all the routes for the application
for app_router in routers:
    app.include_router(app_router)


#Spin up all the models that is needed to be created
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.post("/token", response_model= UserLoginResponse)
async def login(form_data: UserLoginRequest, db: Session = Depends(get_db)):

    print('form_data', form_data)

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
        token=access_token
    )

    db.add(update_user_token)
    db.commit()
    db.refresh(update_user_token)

    return UserLoginResponse(access_token=access_token, user=user)

@app.get("/current-user", response_model=UserResponse)
async def get_current_user_route(_: UserResponse = Depends(get_current_user)):
    return user_id_ctx.get()


@app.post("/logout", response_model=DefaultResponse)
async def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    token_entry = await db.query(UserTokenModel).filter(UserTokenModel.token == token.access_token and UserTokenModel.user_id == user_id_ctx.get('user_id')).first()

    if token_entry:
        token_entry.is_revoked = True
    
    db.commit()

    return DefaultResponse(title="Success", message="Successfully logged out and token revoked")

