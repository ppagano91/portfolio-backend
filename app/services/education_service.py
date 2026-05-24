from app.core.errors import NotFoundError
from app.models.education import Education
from app.repositories.education_repository import EducationRepository
from app.schemas.course import CoursePublic
from app.schemas.education import EducationCreate, EducationPublic, EducationRead, EducationUpdate


class EducationService:
    def __init__(self, education_repo: EducationRepository) -> None:
        self.education_repo = education_repo

    def _to_public(self, education: Education) -> EducationPublic:
        return EducationPublic.model_validate(education)

    def list_education(self, *, published_only: bool = True) -> list[EducationPublic]:
        records = self.education_repo.get_all(published_only=published_only)
        return [self._to_public(record) for record in records]

    def list_courses(self, *, published_only: bool = True) -> list[CoursePublic]:
        records = self.education_repo.get_courses(published_only=published_only)
        return [CoursePublic.from_education(record) for record in records]

    def get_public_course(self, course_id: int) -> CoursePublic:
        course = self.education_repo.get_course_by_id(course_id)
        if not course or not course.published:
            raise NotFoundError("Curso", course_id)
        return CoursePublic.from_education(course)

    def get_education(
        self,
        education_id: int,
        *,
        published_only: bool = False,
    ) -> EducationRead:
        education = self.education_repo.get_by_id(education_id)
        if not education:
            raise NotFoundError("Educación", education_id)
        if published_only and not education.published:
            raise NotFoundError("Educación", education_id)
        return EducationRead.model_validate(education)

    def get_public_education(self, education_id: int) -> EducationPublic:
        education = self.education_repo.get_by_id(education_id)
        if not education or not education.published:
            raise NotFoundError("Educación", education_id)
        return self._to_public(education)

    def create_education(self, data: EducationCreate) -> EducationRead:
        education = Education(**data.model_dump())
        if education.is_current:
            education.end_date = None
        created = self.education_repo.create(education)
        return EducationRead.model_validate(created)

    def update_education(self, education_id: int, data: EducationUpdate) -> EducationRead:
        education = self.education_repo.get_by_id(education_id)
        if not education:
            raise NotFoundError("Educación", education_id)

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(education, field, value)

        if education.is_current:
            education.end_date = None

        updated = self.education_repo.update(education)
        return EducationRead.model_validate(updated)

    def delete_education(self, education_id: int) -> None:
        education = self.education_repo.get_by_id(education_id)
        if not education:
            raise NotFoundError("Educación", education_id)
        self.education_repo.delete(education)
