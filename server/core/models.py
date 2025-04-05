from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from core.constants import RoleType, ApplicationStatus, DegreeType, CourseType, MajorType, CourseEnrollmentStatus, TranscriptRequestStatus, DeliveryMethod, FileCategoryStatus
from config.database import Base  # Assuming you have a Base model from your DB setup

# Base model for common attributes
class BaseModel(Base):
    __abstract__ = True  # This will not create a separate table
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

# ------------------------- USERS & AUTHENTICATION -------------------------

class ApplicationModel(BaseModel):
    __tablename__ = 'applications'

    application_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    reference_number = Column(String(100))
    degree = Column(Enum(DegreeType), nullable=False)
    major = Column(Enum(MajorType), nullable=False)
    role = Column(Enum(RoleType), nullable=False)
    application_status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING, nullable=False)

class UserModel(BaseModel):
    """
    Represents users in the system, storing their login credentials and role.
    """
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    email = Column(String(256), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    role = Column(Enum(RoleType), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    students = relationship("StudentModel", back_populates="user", uselist=False)
    professors = relationship("ProfessorModel", back_populates="user", uselist=False)


class UserTokenModel(Base):
    """
    Stores authentication tokens for user sessions.
    """
    __tablename__ = 'user_tokens'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    is_revoked = Column(Boolean, default=False)

# ------------------------- STUDENTS & PROFESSORS -------------------------

class StudentModel(BaseModel):
    """
    Stores student-specific details.
    """
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    degree = Column(Enum(DegreeType), nullable=False)
    major = Column(Enum(MajorType), nullable=False)
    is_enrolled = Column(Boolean, default=True)

    # Relationships
    user = relationship("UserModel", back_populates="students")
    enrollments = relationship("StudentCourseEnrollmentModel", back_populates="student")
    submissions = relationship("AssignmentSubmissionsModel", back_populates="student")



class ProfessorModel(BaseModel):
    """
    Stores professor-specific details.
    """
    __tablename__ = 'professors'

    professor_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    degree = Column(Enum(DegreeType), nullable=False)
    department = Column(Enum(MajorType), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    user = relationship("UserModel", back_populates="professors")
    assignments = relationship("AssignmentsModel", back_populates="professor")
    sections = relationship("SectionsModel", back_populates="professor")

# ------------------------- COURSES & ENROLLMENT -------------------------

class CoursesModel(BaseModel):
    """
    Stores course details including credit information and prerequisites.
    """
    __tablename__ = 'courses'

    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_code = Column(String(50), unique=True, nullable=False)
    course_name = Column(String(100), nullable=False)
    course_type = Column(Enum(CourseType), nullable=False)
    credits = Column(Integer, nullable=False)

    # Relationships
    sections = relationship("SectionsModel", back_populates="course")

"""
Defines prerequisite relationships between courses - class CoursePrerequisiteMappingModel(BaseModel):
Using Neo4J for this please refer that
"""


class SectionsModel(BaseModel):
    """
    Represents individual course sections assigned to professors.
    """
    __tablename__ = 'sections'

    section_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.course_id', ondelete="CASCADE"), nullable=False)
    professor_id = Column(Integer, ForeignKey('professors.professor_id', ondelete="SET NULL"))
    semester = Column(String(20), nullable=False)
    year = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    enrolled_students = Column(Integer, default=0)

    # Relationships
    course = relationship("CoursesModel", back_populates="sections")
    professor = relationship("ProfessorModel", back_populates="sections")
    enrollments = relationship("StudentCourseEnrollmentModel", back_populates="section")
    assignments = relationship("AssignmentsModel", back_populates="section")


class StudentCourseEnrollmentModel(BaseModel):
    """
    Tracks student enrollment in specific sections.
    """
    __tablename__ = 'student_course_enrollment'

    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id', ondelete="CASCADE"), nullable=False)
    section_id = Column(Integer, ForeignKey('sections.section_id', ondelete="CASCADE"), nullable=False)
    grade = Column(Enum('A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F', name='grade_scale'))
    status = Column(Enum(CourseEnrollmentStatus), nullable=False)

    # Relationships
    student = relationship("StudentModel", back_populates="enrollments")
    section = relationship("SectionsModel", back_populates="enrollments")

# ------------------------- ASSIGNMENTS & SUBMISSION -------------------------

class AssignmentsModel(BaseModel):
    """
    Represents assignments created by professors for specific course sections.
    """
    __tablename__ = 'assignments'

    assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    section_id = Column(Integer, ForeignKey('sections.section_id', ondelete='CASCADE'), nullable=False)
    professor_id = Column(Integer, ForeignKey('professors.professor_id', ondelete='CASCADE'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    due_date = Column(DateTime, nullable=False)
    file_url = Column(String(255), nullable=True)  # Optional: Professors can attach documents

    # Relationships
    section = relationship("SectionsModel", back_populates="assignments")  # Links to Sections
    professor = relationship("ProfessorModel", back_populates="assignments")  # Links to Professors
    submissions = relationship("AssignmentSubmissionsModel", back_populates="assignment", cascade="all, delete")

class AssignmentSubmissionsModel(BaseModel):
    """
    Represents student submissions for assignments.
    """
    __tablename__ = 'assignment_submissions'

    submission_id = Column(Integer, primary_key=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey('assignments.assignment_id', ondelete='CASCADE'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    file_url = Column(String(255), nullable=True)  # URL to uploaded documents
    text_submission = Column(Text, nullable=True)  # Student's typed answer
    submitted_at = Column(DateTime, default=datetime.utcnow)
    grade = Column(String(10), nullable=True)  # Grade assigned by the professor
    feedback = Column(Text, nullable=True)  # Optional: Professor's feedback

    # Relationships
    assignment = relationship("AssignmentsModel", back_populates="submissions")  # Links to Assignments
    student = relationship("StudentModel", back_populates="submissions")  # Links to Students



# ------------------------- TRANSCRIPTS & DOCUMENTS -------------------------

class TranscriptRequestModel(BaseModel):
    """
    Captures student requests for official transcripts.
    """
    __tablename__ = 'transcript_requests'

    request_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id', ondelete="CASCADE"), nullable=False)
    request_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(TranscriptRequestStatus), default='PENDING')
    delivery_method = Column(Enum(DeliveryMethod), nullable=False)


class DocumentsModel(BaseModel):
    """
    Stores documents related to transcripts and other files.
    """
    __tablename__ = 'documents'

    document_id = Column(Integer, primary_key=True, autoincrement=True)
    reference_id = Column(Integer, index=True, nullable=False)
    reference_name = Column(Enum(FileCategoryStatus), nullable=False)
    file_name = Column(String(100), nullable=False)
    bucket_name = Column(String(100), nullable=False)
    reference_link = Column(String(200), nullable=False)
    extension = Column(String(10), nullable=False)