from fastapi import FastAPI, HTTPException, Depends,status
from database import engine
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from models import UserModel, UserTokenModel, Base
from database import get_db
from auth import authenticate_user, create_access_token, get_hashed_password, get_current_user, oauth2_scheme
from schemas import UserCreateRequest, UserResponse
from UserMiddleware import UserMiddleware

#Instantiate the fastapi app
app = FastAPI()

app.add_middleware(UserMiddleware)

#Spin up all the models that is needed to be created
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = authenticate_user(form_data.username, form_data.password, db)

    print('access_token', user)
    
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

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user)
    }

@app.post("/create-user", response_model=UserResponse)
async def create_user(user_data: UserCreateRequest, db: Session = Depends(get_db),):

    hashed_password = get_hashed_password(user_data.password)

    db_user = UserModel(
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        role=user_data.role,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse.model_validate(db_user)

@app.get("/current-user", response_model=UserResponse)
async def get_current_user_route(current_user: UserResponse = Depends(get_current_user)):
    return current_user

@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme), current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    
    token_entry = db.query(UserTokenModel).filter(UserTokenModel.user_token == token and UserTokenModel.user_id == current_user.user_id).first()

    if token_entry:
        token_entry.is_revoked = True
    
    db.commit()

    return {"detail": "Successfully logged out and token revoked"}

