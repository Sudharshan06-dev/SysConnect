from enum import Enum


SUCCESS = "Success"

ERROR = "Error"


#Enum Types
class RoleType(Enum):
    STUDENT = 'STUDENT'
    PROFESSOR = 'PROFESSOR'

class RoleTypeWithAdmin(Enum):
    STUDENT = 'STUDENT'
    PROFESSOR = 'PROFESSOR'
    ADMIN = 'ADMIN'

class ApplicationStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

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