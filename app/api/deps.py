from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.contact_repository import ContactRepository
from app.repositories.dashboard_repository import DashboardRepository
from app.repositories.notebook_repository import NotebookRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.technology_repository import TechnologyRepository
from app.services.contact_service import ContactService
from app.services.dashboard_service import DashboardService
from app.services.notebook_service import NotebookService
from app.services.project_service import ProjectService
from app.services.technology_service import TechnologyService


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    return ProjectService(ProjectRepository(db), TechnologyRepository(db))


def get_technology_service(db: Session = Depends(get_db)) -> TechnologyService:
    return TechnologyService(TechnologyRepository(db))


def get_dashboard_service(db: Session = Depends(get_db)) -> DashboardService:
    return DashboardService(DashboardRepository(db), ProjectRepository(db))


def get_notebook_service(db: Session = Depends(get_db)) -> NotebookService:
    return NotebookService(NotebookRepository(db), ProjectRepository(db))


def get_contact_service(db: Session = Depends(get_db)) -> ContactService:
    return ContactService(ContactRepository(db))
