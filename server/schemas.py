from pydantic import BaseModel
from constants import RoleType

# BaseModel => This is from Pydantic not from the database.py file
# from_attributes = True => Allows Pydantic models to map attributes directly from SQLAlchemy models.
# Check Info.txt  => for further explanation

''' RESPONSE FUNCTIONS'''
class DefaultResponse(BaseModel):
    title: str
    message: str


# User Login Data
class UserResponse(BaseModel):
    user_id: int
    firstname: str
    lastname: str
    email: str
    username: str
    role: RoleType

    class Config:
        from_attributes  = True

# User Login along with access token for authentication
class UserLoginResponse(BaseModel):
    access_token: str
    user: UserResponse


''' REQUEST FUNCTIONS'''

class CreateUserRequest(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str
    username: str
    role: RoleType