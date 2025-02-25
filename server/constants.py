from enum import Enum

SECRET_KEY = "dd4005a7c2fee0352b7268cedcf9e36dcadc11d57bf77974875a21e108fb5277"
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

'''
class DegreeType(Enum):
#     FRESHMAN = 'FRESHMAN',
#     SOPHOMORE = 'SOPHOMORE', 
#     JUNIOR = 'JUNIOR', 
#     SENIOR = 'SENIOR', 
#     UNDERGRADUATE = 'UNDERGRADUATE', 
#     GRADUATE = 'GRADUATE', 
#     POSTGRADUATE = 'POSTGRADUATE'
'''