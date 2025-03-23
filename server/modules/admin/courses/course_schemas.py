from pydantic import BaseModel
from core.constants import DegreeType, MajorType, CourseType
from typing import List, Optional

class CourseCreateSchema(BaseModel):
    course_id: Optional[int] = None
    course_number: int
    course_name: str
    course_for: DegreeType
    course_type: CourseType
    major: MajorType
    credits: int
    prerequisite_number: Optional[int]

class PrerequisiteSchema(BaseModel):
    course_number: int
    prerequisite_course_number: int

class PrerequisiteResponse(BaseModel):
    course_number: int
    prerequisites: List[int]