from enum import Enum

SECRET_KEY = "123456789463543"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 60 * 60


#Enum Types
class RoleType(Enum):
    STUDENT = 'STUDENT'
    PROFESSOR = 'PROFESSOR'

class RoleTypeWithAdmin(Enum):
    STUDENT = 'STUDENT'
    PROFESSOR = 'PROFESSOR'
    ADMIN = 'ADMIN'


class DegreeType(Enum):
    BACHELORS = 'BACHELORS', 
    GRADUATE = 'GRADUATE', 
    POSTGRADUATE = 'POSTGRADUATE'

class CourseEnrollmentStatus(Enum):
    ENROLLED = 'ENROLLED',
    COMPLETED = 'COMPLETED',
    DROPPED = 'DROPPED'

class DeliveryMethod(Enum):
    EMAIL = 'EMAIL'
    PRINTED = 'PRINTED',
    BOTH = 'BOTH'
                      
class TranscriptRequestStatus(Enum):
    PENDING = 'PENDING',
    PROCESSING = 'PROCESSING',
    COMPLETED = 'COMPLETED',
    REJECTED = 'REJECTED'