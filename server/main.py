from fastapi import FastAPI, HTTPException, Depends,status, Response,  Form, Request
from fastapi.responses import RedirectResponse
from core.database import engine
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from core.models import UserTokenModel, Base, UserModel
from core.database import get_db
from core.auth import authenticate_user, create_access_token, oauth2_scheme, get_hashed_password 
from core.schemas import UserResponse, UserLoginResponse, DefaultResponse
from core.user_middleware import user_middleware
from login import router as login_router
from admin import admin_router, AdminMiddleware as admin_middleware
from core.context_vars import user_id_ctx
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from jose import jwt, JWTError
import core.auth
import os

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

# Mount the 'client' directory to serve static files
app.mount("/static", StaticFiles(directory="../client/src/app/homepage"), name="static")
@app.get("/")
async def root():
    return FileResponse("../client/src/app/homepage/homepage.component.html")

# Serve the signup.html when navigating to /signup
@app.get("/signup")
def read_signup():
    return FileResponse("../client/src/app/homepage/signup.html")

@app.post("/signup", response_model=DefaultResponse) # New signup endpoint
async def signup(request: Request, username: str = Form(...), password: str = Form(...), email: str = Form(...), role: str = Form(...), firstname: str = Form(...), lastname: str = Form(...), db: Session = Depends(get_db)):
    try:
        existing_user = db.query(UserModel).filter(UserModel.username == username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        hashed_password = get_hashed_password(password)
        new_user = UserModel(username=username, hashed_password=hashed_password, email=email, role=role, firstname=firstname, lastname=lastname)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        #return DefaultResponse(title="Success", message="User registered successfully")
        return RedirectResponse(url="/static/homepage.component.html", status_code=status.HTTP_302_FOUND)

    except Exception as e:
        print(f"Error during signup: {e}") #Print the error to the console.
        db.rollback() #Rollback the transaction to avoid partial database changes.
        raise HTTPException(status_code=500, detail="Internal server error during signup.")


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

    return UserLoginResponse(access_token=access_token, user=UserResponse.model_validate(user))

@app.get("/landing") #Landing page endpoint.
async def landing(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    #Verify token and user.
    try:
        payload = jwt.decode(token, core.auth.AUTH_SECRET_KEY, algorithms=[core.auth.AUTH_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(UserModel).filter(UserModel.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        #If token is valid, serve landing page.
        return FileResponse("../client/src/app/homepage/landing.component.html") #Adjust path.
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/logout", response_model=DefaultResponse)
async def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    token_entry = await db.query(UserTokenModel).filter(UserTokenModel.user_token == token.access_token and UserTokenModel.user_id == user_id_ctx.get('user_id')).first()

    if token_entry:
        token_entry.is_revoked = True
    
    db.commit()

    return DefaultResponse(title="Success", message="Successfully logged out and token revoked")

