from pydantic import BaseModel
from utility import RoleType

class UserResponse(BaseModel):
    user_id: int
    firstname: str
    lastname: str
    email: str
    username: str
    role: RoleType

    class Config:
        from_attributes  = True

class UserCreateRequest(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str
    username: str
    role: RoleType