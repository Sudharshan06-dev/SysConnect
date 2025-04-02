from enum import Enum


SUCCESS = "Success"

ERROR = "Error"


#Enum Types
class RoleType(str, Enum):
    STUDENT = 'STUDENT'
    PROFESSOR = 'PROFESSOR'
    POTENTIAL_STUDENT = 'POTENTIAL_STUDENT'
    POTENTIAL_PROFESSOR = 'POTENTIAL PROFESSOR'
    ADMIN = 'ADMIN'

class ApplicationStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class DegreeType(str, Enum):
    BACHELORS = 'BACHELORS'
    MASTERS = 'MASTERS'
    POSTDOCTORATE = 'POSTDOCTORATE'

class CourseType(str, Enum):
    CORE = 'CORE'
    ELECTIVE = 'ELECTIVE'

class MajorPrefix(str, Enum):
    COMPUTER_SCIENCE = 'CPSC'
    SOFTWARE_ENGINEERING = 'SW'

class MajorType(str, Enum):
    COMPUTER_SCIENCE = 'COMPUTER_SCIENCE'
    SOFTWARE_ENGINEERING = 'SOFTWARE_ENGINEERING'

class CourseEnrollmentStatus(str, Enum):
    ENROLLED = 'ENROLLED'
    COMPLETED = 'COMPLETED'
    DROPPED = 'DROPPED'

class DeliveryMethod(str, Enum):
    EMAIL = 'EMAIL'
    PRINTED = 'PRINTED'
    BOTH = 'BOTH'

class NotificationMethod(str, Enum):
    REMINDER = 'REMINDER'
    SYSTEM = 'SYSTEM'
    GRADE_UPDATE = 'GRADE_UPDATE'
                      
class TranscriptRequestStatus(str, Enum):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'
    REJECTED = 'REJECTED'

class FileCategoryStatus(str, Enum):
    COURSE = 'COURSE'
    ASSIGNMENT_SUBMISSION = 'ASSIGNMENT_SUBMISSION'
    ASSIGNMENT = 'ASSIGNMENT'