from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum, ForeignKey
from config.database import Base
from uuid import uuid4
from core.constants import RoleType, RoleTypeWithAdmin, DegreeType, CourseType, CourseEnrollmentStatus, TranscriptRequestStatus, DeliveryMethod, ApplicationStatus, MajorType

class BaseModel(Base):
    __abstract__ = True  # Ensures this class is not treated as a table
    __allow_unmapped__ = True  # Allows using old-style Column()
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, unique=False, default=False)


class UserTokenModel(Base):
    __tablename__ = 'user_tokens'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    user_token = Column(String(255), unique=True)
    is_revoked = Column(Boolean, unique=False, default=False)

class ApplicationModel(BaseModel):
    __tablename__ = 'applications'

    application_id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(100))
    lastname = Column(String(100))
    reference_number = Column(String(100), default=uuid4())
    email = Column(String(256), unique=True, index=True)
    username = Column(String(100), unique=True)
    hashed_password = Column(String(256))
    role = Column(Enum(RoleType), nullable=False)
    application_status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING, nullable=False)


class UserModel(BaseModel):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(100), unique=False)
    lastname = Column(String(100), unique=False)
    email = Column(String(256), unique=True, index=True)
    username = Column(String(100), unique=True)
    hashed_password = Column(String(256))
    role = Column(Enum(RoleTypeWithAdmin), nullable=False)
    active_user = Column(Boolean, unique=False, default=True)

# Students Table: Stores student details, including major, degree level, and account status.
class StudentsModel(BaseModel):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    degree = Column(Enum(DegreeType), nullable=False)
    major = Column(String(100), nullable=False)
    account_enabled = Column(Boolean, default=True)

# Professors Table: Stores professor details, including academic qualifications and assigned major.
class ProfessorsModel(BaseModel):
    __tablename__ = 'professors'

    professor_id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    degree_earned = Column(Enum(DegreeType), nullable=False)
    major = Column(String(100), nullable=False)
    account_enabled = Column(Boolean, default=True)

# Courses Table: Stores course details, including the degree level it applies to and its credit value.
class CoursesModel(BaseModel):
    __tablename__ = 'courses'

    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_number = Column(String(100), nullable=False)
    course_name = Column(String(100), nullable=False)
    course_type = Column(Enum(CourseType), default='CORE', nullable=False)
    course_for = Column(Enum(DegreeType), nullable=False)
    major = Column(Enum(MajorType), nullable=False)
    credits = Column(Integer, nullable=False)
    
# Course Prerequisites Mapping: Defines prerequisite relationships between courses to enforce enrollment rules.
class CoursePrerequisiteMappingModel(BaseModel):
    __tablename__ = 'course_prerequisites_mapping'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False)
    prerequisite_course_id = Column(Integer, ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False)

# Sections Table: Represents individual class sections for a course, each assigned to a professor and semester.
class SectionsModel(BaseModel):
    __tablename__ = 'sections'

    section_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False)
    professor_id = Column(Integer, ForeignKey('professors.professor_id', ondelete='SET NULL'))
    semester = Column(String(20), nullable=False)
    year = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    enrolled_students = Column(Integer, default=0)

# Student Course Enrollment: Tracks student enrollment in specific sections, their grades, and enrollment status.
class StudentCourseEnrollmentModel(BaseModel):
    __tablename__ = 'student_course_enrollment'

    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    section_id = Column(Integer, ForeignKey('sections.section_id', ondelete='CASCADE'), nullable=False)
    grades_earned = Column(Enum('A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F'))
    status = Column(Enum(CourseEnrollmentStatus), default='ENROLLED', nullable=False)

# Degree Requirements: Lists required courses for each major to validate graduation eligibility.
class DegreeRequirementModel(Base):
    __tablename__ = 'degree_requirements'

    requirement_id = Column(Integer, primary_key=True, autoincrement=True)
    major = Column(String(100), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Transcript Requests: Captures student requests for official transcripts and tracks processing status.
class TranscriptRequestModel(BaseModel):
    __tablename__ = 'transcript_requests'

    request_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    request_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(TranscriptRequestStatus), default='PENDING')
    delivery_method = Column(Enum(DeliveryMethod), nullable=False)