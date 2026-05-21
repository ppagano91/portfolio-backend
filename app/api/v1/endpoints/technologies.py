from fastapi import APIRouter, Depends, status

from app.api.deps import get_technology_service
from app.schemas.common import ApiResponse, success_response
from app.schemas.technology import TechnologyCreate, TechnologyRead
from app.services.technology_service import TechnologyService

router = APIRouter(prefix="/technologies", tags=["technologies"])


@router.get("", response_model=ApiResponse[list[TechnologyRead]])
def list_technologies(
    service: TechnologyService = Depends(get_technology_service),
) -> ApiResponse[list[TechnologyRead]]:
    technologies = service.list_technologies()
    return success_response(technologies)


@router.post("", response_model=ApiResponse[TechnologyRead], status_code=status.HTTP_201_CREATED)
def create_technology(
    payload: TechnologyCreate,
    service: TechnologyService = Depends(get_technology_service),
) -> ApiResponse[TechnologyRead]:
    technology = service.create(payload)
    return success_response(technology, message="Tecnología creada correctamente")
