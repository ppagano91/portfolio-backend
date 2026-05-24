from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.education import Education, EducationType


class EducationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _ordered(self, stmt):
        return stmt.order_by(
            Education.sort_order.asc(),
            Education.end_date.desc().nulls_first(),
            Education.start_date.desc().nulls_last(),
        )

    def get_all(self, *, published_only: bool = True) -> list[Education]:
        stmt = select(Education)
        if published_only:
            stmt = stmt.where(Education.published.is_(True))
        return list(self.db.scalars(self._ordered(stmt)).all())

    def get_courses(self, *, published_only: bool = True) -> list[Education]:
        stmt = select(Education).where(Education.education_type == EducationType.COURSE)
        if published_only:
            stmt = stmt.where(Education.published.is_(True))
        return list(self.db.scalars(self._ordered(stmt)).all())

    def get_course_by_id(self, course_id: int) -> Education | None:
        stmt = select(Education).where(
            Education.id == course_id,
            Education.education_type == EducationType.COURSE,
        )
        return self.db.scalar(stmt)

    def get_by_id(self, education_id: int) -> Education | None:
        stmt = select(Education).where(Education.id == education_id)
        return self.db.scalar(stmt)

    def create(self, education: Education) -> Education:
        self.db.add(education)
        self.db.commit()
        self.db.refresh(education)
        return education

    def update(self, education: Education) -> Education:
        self.db.commit()
        self.db.refresh(education)
        return education

    def delete(self, education: Education) -> None:
        self.db.delete(education)
        self.db.commit()
