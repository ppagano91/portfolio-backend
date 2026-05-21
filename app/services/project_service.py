from geoalchemy2.shape import to_shape

from app.core.errors import BadRequestError, NotFoundError
from app.models.project import Project
from app.repositories.project_repository import ProjectRepository
from app.repositories.technology_repository import TechnologyRepository
from app.schemas.dashboard import DashboardRead
from app.schemas.notebook import NotebookRead
from app.schemas.project import (
    ProjectCreate,
    ProjectDetailRead,
    ProjectLocationRead,
    ProjectRead,
    ProjectUpdate,
)
from app.utils.slug import ensure_unique_slug, slugify


class ProjectService:
    def __init__(
        self,
        project_repo: ProjectRepository,
        technology_repo: TechnologyRepository,
    ) -> None:
        self.project_repo = project_repo
        self.technology_repo = technology_repo

    def list_projects(self, *, published_only: bool = True) -> list[Project]:
        return self.project_repo.get_all(published_only=published_only)

    def list_featured(self) -> list[Project]:
        return self.project_repo.get_all(published_only=True, featured_only=True)

    def get_by_slug(self, slug: str) -> Project:
        project = self.project_repo.get_by_slug(slug)
        if not project:
            raise NotFoundError("Proyecto", slug)
        return project

    def _location_to_read(self, location) -> ProjectLocationRead:
        latitude, longitude = None, None
        if location.geom is not None:
            point = to_shape(location.geom)
            longitude, latitude = point.x, point.y
        return ProjectLocationRead(
            id=location.id,
            name=location.name,
            description=location.description,
            latitude=latitude,
            longitude=longitude,
        )

    def get_detail_by_slug(self, slug: str) -> ProjectDetailRead:
        project = self.project_repo.get_by_slug(slug, with_details=True)
        if not project:
            raise NotFoundError("Proyecto", slug)
        base = ProjectRead.model_validate(project)
        return ProjectDetailRead(
            **base.model_dump(),
            dashboards=[DashboardRead.model_validate(d) for d in project.dashboards],
            notebooks=[NotebookRead.model_validate(n) for n in project.notebooks],
            locations=[self._location_to_read(loc) for loc in project.locations],
        )

    def get_by_id(self, project_id: int) -> Project:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise NotFoundError("Proyecto", project_id)
        return project

    def _resolve_technologies(self, technology_ids: list[int]) -> list:
        technologies = self.technology_repo.get_by_ids(technology_ids)
        if len(technologies) != len(set(technology_ids)):
            raise BadRequestError("Una o más tecnologías no existen", code="INVALID_TECHNOLOGY")
        return technologies

    def _build_slug(self, title: str, slug: str | None) -> str:
        base_slug = slugify(slug or title)
        return ensure_unique_slug(base_slug, self.project_repo.get_all_slugs())

    def create(self, data: ProjectCreate) -> Project:
        slug = self._build_slug(data.title, data.slug)
        project = Project(
            title=data.title,
            slug=slug,
            summary=data.summary,
            description=data.description,
            project_type=data.project_type,
            status=data.status,
            cover_image_url=data.cover_image_url,
            repository_url=data.repository_url,
            demo_url=data.demo_url,
            documentation_url=data.documentation_url,
            featured=data.featured,
            published=data.published,
        )
        if data.technology_ids:
            project.technologies = self._resolve_technologies(data.technology_ids)
        return self.project_repo.create(project)

    def update(self, project_id: int, data: ProjectUpdate) -> Project:
        project = self.get_by_id(project_id)
        update_data = data.model_dump(exclude_unset=True)
        technology_ids = update_data.pop("technology_ids", None)

        if "slug" in update_data or "title" in update_data:
            new_slug = update_data.get("slug") or project.slug
            if "title" in update_data and "slug" not in update_data:
                new_slug = slugify(update_data["title"])
            existing_slugs = [
                s for s in self.project_repo.get_all_slugs() if s != project.slug
            ]
            update_data["slug"] = ensure_unique_slug(slugify(new_slug), existing_slugs)

        for field, value in update_data.items():
            setattr(project, field, value)

        if technology_ids is not None:
            project.technologies = self._resolve_technologies(technology_ids)

        return self.project_repo.update(project)

    def delete(self, project_id: int) -> None:
        project = self.get_by_id(project_id)
        self.project_repo.delete(project)
