from app.core.errors import ConflictError
from app.models.technology import Technology
from app.repositories.technology_repository import TechnologyRepository
from app.schemas.technology import TechnologyCreate


class TechnologyService:
    def __init__(self, technology_repo: TechnologyRepository) -> None:
        self.technology_repo = technology_repo

    def list_technologies(self) -> list[Technology]:
        return self.technology_repo.get_all()

    def create(self, data: TechnologyCreate) -> Technology:
        existing = self.technology_repo.get_by_name(data.name)
        if existing:
            raise ConflictError(f"La tecnología '{data.name}' ya existe")
        technology = Technology(
            name=data.name,
            category=data.category,
            icon_url=data.icon_url,
        )
        return self.technology_repo.create(technology)
