from fastapi import APIRouter, Depends

from app.api.deps import get_education_service
from app.schemas.common import ApiResponse, success_response
from app.schemas.course import CoursePublic
from app.services.education_service import EducationService

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=ApiResponse[list[CoursePublic]])
def list_courses(
    service: EducationService = Depends(get_education_service),
) -> ApiResponse[list[CoursePublic]]:
    courses = service.list_courses(published_only=True)
    return success_response(courses, message="Cursos obtenidos correctamente")


@router.get("/{course_id}", response_model=ApiResponse[CoursePublic])
def get_course(
    course_id: int,
    service: EducationService = Depends(get_education_service),
) -> ApiResponse[CoursePublic]:
    course = service.get_public_course(course_id)
    return success_response(course, message="Curso obtenido correctamente")
