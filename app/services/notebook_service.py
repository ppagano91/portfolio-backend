from app.core.errors import BadRequestError, NotFoundError
from app.models.notebook import Notebook
from app.repositories.notebook_repository import NotebookRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.notebook import NotebookCreate


class NotebookService:
    def __init__(
        self,
        notebook_repo: NotebookRepository,
        project_repo: ProjectRepository,
    ) -> None:
        self.notebook_repo = notebook_repo
        self.project_repo = project_repo

    def list_notebooks(self) -> list[Notebook]:
        return self.notebook_repo.get_all()

    def get_by_id(self, notebook_id: int) -> Notebook:
        notebook = self.notebook_repo.get_by_id(notebook_id)
        if not notebook:
            raise NotFoundError("Notebook", notebook_id)
        return notebook

    def _validate_project(self, project_id: int | None) -> None:
        if project_id is not None and not self.project_repo.get_by_id(project_id):
            raise BadRequestError("El proyecto asociado no existe", code="INVALID_PROJECT")

    def create(self, data: NotebookCreate) -> Notebook:
        self._validate_project(data.project_id)
        notebook = Notebook(
            title=data.title,
            description=data.description,
            notebook_url=data.notebook_url,
            repository_url=data.repository_url,
            project_id=data.project_id,
        )
        return self.notebook_repo.create(notebook)
