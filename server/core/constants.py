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
    BACHELORS = 'BACHELORS'
    MASTERS = 'MASTERS'
    POSTDOCTORATE = 'POSTDOCTORATE'

class CourseType(Enum):
    CORE = 'CORE'
    ELECTIVE = 'ELECTIVE'

class MajorPrefix(Enum):
    COMPUTER_SCIENCE = 'CPSC'
    SOFTWARE_ENGINEERING = 'SW'
    MECHANICAL = 'MECH'
    CIVIL = 'CVL'
    ELECTRICAL = 'EEE'

class MajorType(Enum):
    COMPUTER_SCIENCE = 'COMPUTER_SCIENCE'
    SOFTWARE_ENGINEERING = 'SOFTWARE_ENGINEERING'
    MECHANICAL = 'MECHANICAL'
    CIVIL = 'CIVIL'
    ELECTRICAL = 'ELECTRICAL'

class CourseEnrollmentStatus(Enum):
    ENROLLED = 'ENROLLED'
    COMPLETED = 'COMPLETED'
    DROPPED = 'DROPPED'

class DeliveryMethod(Enum):
    EMAIL = 'EMAIL'
    PRINTED = 'PRINTED'
    BOTH = 'BOTH'
                      
class TranscriptRequestStatus(Enum):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'
    REJECTED = 'REJECTED'