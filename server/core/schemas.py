from pydantic import BaseModel, EmailStr
from core.constants import RoleType, ApplicationStatus, DegreeType, MajorType
from typing import Optional

# BaseModel => This is from Pydantic not from the database.py file
# from_attributes = True => Allows Pydantic models to map attributes directly from SQLAlchemy models.
# Check Info.txt  => for further explanation

''' RESPONSE FUNCTIONS'''
class DefaultResponse(BaseModel):
    title: str
    message: str


# User Login Data
class ApplicationResponse(BaseModel):
    application_id: int
    user_id: int
    reference_number:str
    role: RoleType
    degree: Optional[DegreeType] = None
    major: Optional[MajorType] = None
    application_status: ApplicationStatus
    

    class Config:
        from_attributes  = True

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

class UserLoginRequest(BaseModel):
    username: str
    password: str
    
class CreateApplicationUserRequest(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str
    confirmPassword: str
    username: str
    role: RoleType
    degree: Optional[DegreeType] = None
    major: Optional[MajorType] = None

class ApproveRequest(BaseModel):
    email: EmailStr

class BulkApproveRequest(BaseModel):
    application_id: int
    emails: EmailStr