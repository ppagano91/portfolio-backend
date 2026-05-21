from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _base_query(self):
        return select(Project).options(selectinload(Project.technologies))

    def get_all(
        self,
        *,
        published_only: bool = False,
        featured_only: bool = False,
    ) -> list[Project]:
        stmt = self._base_query()
        if published_only:
            stmt = stmt.where(Project.published.is_(True))
        if featured_only:
            stmt = stmt.where(Project.featured.is_(True))
        stmt = stmt.order_by(Project.created_at.desc())
        return list(self.db.scalars(stmt).all())

    def get_by_slug(self, slug: str) -> Project | None:
        stmt = self._base_query().where(Project.slug == slug)
        return self.db.scalar(stmt)

    def get_by_id(self, project_id: int) -> Project | None:
        stmt = self._base_query().where(Project.id == project_id)
        return self.db.scalar(stmt)

    def get_all_slugs(self) -> list[str]:
        stmt = select(Project.slug)
        return list(self.db.scalars(stmt).all())

    def create(self, project: Project) -> Project:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return self.get_by_id(project.id)  # type: ignore[return-value]

    def update(self, project: Project) -> Project:
        self.db.commit()
        self.db.refresh(project)
        return self.get_by_id(project.id)  # type: ignore[return-value]

    def delete(self, project: Project) -> None:
        self.db.delete(project)
        self.db.commit()
