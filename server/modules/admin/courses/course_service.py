from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from config.database import get_db
from config.neo4j import neo4j_conn
from core.models import CoursesModel, DegreeType, CourseType
from core.constants import MajorPrefix, SUCCESS, ERROR
from core.auth import get_current_user
from modules.admin.courses.course_schemas import CourseCreateSchema
from core.utility import create_response
import logging

logger = logging.getLogger(__name__)

course_router = APIRouter(prefix='/course')

#CREATE A COURSE & ADD PREREQUISITES
@course_router.post('/create-course', response_class=JSONResponse)
async def create_course(
    course_details: CourseCreateSchema, 
    db: Session = Depends(get_db), 
    _: dict = Depends(get_current_user)
):
    """
    Creates a course and its prerequisites in the database & Neo4j.
    """
    try:

        #Create or Update Courses
        create_course_data = await _create_or_update_course(course_details, db)
        if not create_course_data:
            return create_response(422, "courses_added_failed", ERROR)

        #Create course nodes
        create_course_node = await _add_course_node(course_details.course_number)
        if not create_course_node:
            return create_response(422, "courses_added_failed", ERROR)

        #If Prerequisites exists then
        if course_details.prerequisite_number:

            course_nodes = await _add_course_node(course_details.prerequisite_number)
            if not course_nodes:
                return create_response(422, "courses_added_failed", ERROR)
            
            add_course_connection = await _add_course_prerequisite(course_details.course_number, course_details.prerequisite_number)
            if not add_course_connection:
                return create_response(422, "courses_added_failed", ERROR)

        return create_response(200, "courses_added", SUCCESS)

    except SQLAlchemyError:
        db.rollback()
        logger.exception("Database error in creating courses")
        return create_response(500, "courses_added_failed", ERROR)

    except Exception:
        logger.exception("Unexpected error in creating courses")
        return create_response(500, "courses_added_failed", ERROR)


#DELETE A COURSE
@course_router.delete('/{course_number}', response_class=JSONResponse)
async def delete_course(
    course_number: int, 
    db: Session = Depends(get_db), 
    _: dict = Depends(get_current_user)
):
    """
    Marks a course as deleted in the database and removes its relationships from Neo4j.
    """
    try:
        existing_course = db.query(CoursesModel).filter(CoursesModel.course_number == course_number).first()

        if existing_course:
            existing_course.is_deleted = True
            db.commit()
            db.refresh(existing_course)

            # Remove course from Neo4j
            await _delete_course_node(existing_course.course_number)

        return create_response(200, "course_deleted", SUCCESS)

    except SQLAlchemyError:
        db.rollback()
        logger.exception("Database error in deleting course")
        return create_response(500, "course_deleted_failed", ERROR)

    except Exception:
        logger.exception("Unexpected error in deleting course")
        return create_response(500, "course_deleted_failed", ERROR)


#ADD/UPDATE PREREQUISITES
@course_router.put('/{course_number}/add-prerequisites/{prerequisite_number}', response_class=JSONResponse)
async def add_prerequisites(
    course_number: int, 
    prerequisite_number: int, 
    db: Session = Depends(get_db), 
    _: dict = Depends(get_current_user)
):
    """
    Adds or updates a prerequisite for a course in Neo4j.
    """
    try:

        #Check existing prerequisite number
        existing_prereq = await _get_prerequisites(course_number)

        #If existing prerequisite is not same as prereq number then delete previous connection
        if existing_prereq and existing_prereq != prerequisite_number:
            await _delete_course_connection(course_number, existing_prereq[0])

        #Add the prereq number to the current course
        if not await _add_course_prerequisite(course_number, prerequisite_number):
            return create_response(422, "courses_added_failed", ERROR)

        return create_response(200, "prerequisite_added", SUCCESS)

    except Exception:
        logger.exception("Error in adding prerequisite")
        return create_response(500, "courses_added_failed", ERROR)


#FETCH EXISTING PREREQUISITES
async def _get_prerequisites(course_number: int):
    try:
        query = """
        MATCH (c:Course {number: $course_number})-[:PRE_REQ_FOR]->(p)
        RETURN p.number AS prerequisites;
        """
        result = neo4j_conn.execute_query(query, {"course_number": course_number})
        return result[0]["prerequisites"] if result else []
       
    except Exception:
        logger.exception(f"Error fetching prerequisites for course {course_number}")
        return []


#DELETE A COURSE NODE
async def _delete_course_node(course_number: int):
    try:
        query = "MATCH (c:Course {number: $course_number}) DETACH DELETE c;"
        neo4j_conn.execute_query(query, {"course_number": course_number})
        return True
    except Exception:
        logger.exception(f"Error deleting course {course_number} in Neo4j")
        return False


#DELETE A PREREQUISITE RELATIONSHIP
async def _delete_course_connection(course_number: int, prereq_number: int):
    try:
        query = """
        MATCH (c1:Course {number: $course_number})-[r:PRE_REQ_FOR]->(c2:Course {number: $prereq_number})
        DELETE r;
        """
        neo4j_conn.execute_query(query, {"course_number": course_number, "prereq_number": prereq_number})
        return True
    except Exception:
        logger.exception(f"Error deleting prerequisite relationship: {course_number} -> {prereq_number}")
        return False


#CREATE OR UPDATE A COURSE
async def _create_or_update_course(course_details: CourseCreateSchema, db: Session):
    try:
        existing_course = db.query(CoursesModel).filter(CoursesModel.course_id == course_details.course_id).first()

        #Check if course already exists, if yes, update the course
        if existing_course:
            return await _update_course(existing_course, course_details, db)
        
        #Create the course
        return await _create_course(course_details, db)

    except Exception:
        db.rollback()
        logger.exception("Error in creating/updating course")
        return False


#CREATE A COURSE
async def _create_course(course_details: CourseCreateSchema, db: Session):
    new_course = CoursesModel(
        course_number=course_details.course_number,
        course_name=MajorPrefix[course_details.major.name].value + str(course_details.course_number),
        course_for=DegreeType[course_details.course_for.name].value,
        course_type=CourseType[course_details.course_type.name].value,
        major=course_details.major,
        credits=course_details.credits,
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


#UPDATE A COURSE
async def _update_course(course: CoursesModel, course_details: CourseCreateSchema, db: Session):
    course.course_number = course_details.course_number
    course.course_name = MajorPrefix[course_details.major.name].value + str(course_details.course_number)
    course.course_for = DegreeType[course_details.course_for.name].value
    course.course_type = CourseType[course_details.course_type.name].value
    course.major = course_details.major
    course.credits = course_details.credits

    db.commit()
    db.refresh(course)
    return course

#ADD COURSE NODE TO NEO4J
async def _add_course_node(course_number: int):
    try:
        query = "MERGE (c:Course {number: $number}) RETURN c"
        neo4j_conn.execute_query(query, {"number": course_number})
        return True
    except Exception:
        logger.exception("Error adding course node")
        return False


#ADD PREREQUISITE RELATIONSHIP
async def _add_course_prerequisite(course_number: int, prerequisite_number: int):
    try:
        query = "MATCH (c1:Course {number: $course_number}), (c2:Course {number: $prerequisite_number}) CREATE (c1)-[:PRE_REQ_FOR]->(c2)"
        neo4j_conn.execute_query(query, {"course_number": course_number, "prerequisite_number": prerequisite_number})
        return True
    except Exception:
        logger.exception("Error adding prerequisite")
        return False