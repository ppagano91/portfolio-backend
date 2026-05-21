from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_project_service
from app.schemas.common import ApiResponse, success_response
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=ApiResponse[list[ProjectRead]])
def list_projects(
    published_only: bool = Query(True, description="Filtrar solo proyectos publicados"),
    service: ProjectService = Depends(get_project_service),
) -> ApiResponse[list[ProjectRead]]:
    projects = service.list_projects(published_only=published_only)
    return success_response(projects)


@router.get("/featured", response_model=ApiResponse[list[ProjectRead]])
def list_featured_projects(
    service: ProjectService = Depends(get_project_service),
) -> ApiResponse[list[ProjectRead]]:
    projects = service.list_featured()
    return success_response(projects)


@router.get("/{slug}", response_model=ApiResponse[ProjectRead])
def get_project_by_slug(
    slug: str,
    service: ProjectService = Depends(get_project_service),
) -> ApiResponse[ProjectRead]:
    project = service.get_by_slug(slug)
    return success_response(project)


@router.post("", response_model=ApiResponse[ProjectRead], status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
) -> ApiResponse[ProjectRead]:
    project = service.create(payload)
    return success_response(project, message="Proyecto creado correctamente")


@router.put("/{project_id}", response_model=ApiResponse[ProjectRead])
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
) -> ApiResponse[ProjectRead]:
    project = service.update(project_id, payload)
    return success_response(project, message="Proyecto actualizado correctamente")


@router.delete("/{project_id}", response_model=ApiResponse[None])
def delete_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service),
) -> ApiResponse[None]:
    service.delete(project_id)
    return success_response(None, message="Proyecto eliminado correctamente")
