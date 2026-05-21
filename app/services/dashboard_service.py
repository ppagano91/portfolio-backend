from app.core.errors import BadRequestError, NotFoundError
from app.models.dashboard import Dashboard
from app.repositories.dashboard_repository import DashboardRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.dashboard import DashboardCreate


class DashboardService:
    def __init__(
        self,
        dashboard_repo: DashboardRepository,
        project_repo: ProjectRepository,
    ) -> None:
        self.dashboard_repo = dashboard_repo
        self.project_repo = project_repo

    def list_dashboards(self) -> list[Dashboard]:
        return self.dashboard_repo.get_all()

    def get_by_id(self, dashboard_id: int) -> Dashboard:
        dashboard = self.dashboard_repo.get_by_id(dashboard_id)
        if not dashboard:
            raise NotFoundError("Dashboard", dashboard_id)
        return dashboard

    def _validate_project(self, project_id: int | None) -> None:
        if project_id is not None and not self.project_repo.get_by_id(project_id):
            raise BadRequestError("El proyecto asociado no existe", code="INVALID_PROJECT")

    def create(self, data: DashboardCreate) -> Dashboard:
        self._validate_project(data.project_id)
        dashboard = Dashboard(
            title=data.title,
            description=data.description,
            tool=data.tool,
            embed_url=data.embed_url,
            public_url=data.public_url,
            project_id=data.project_id,
        )
        return self.dashboard_repo.create(dashboard)
