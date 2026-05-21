from fastapi import APIRouter, Depends, status

from app.api.deps import get_experience_service
from app.schemas.common import ApiResponse, success_response
from app.schemas.experience import (
    ExperienceCreate,
    ExperiencePublic,
    ExperienceRead,
    ExperienceUpdate,
)
from app.services.experience_service import ExperienceService

router = APIRouter(prefix="/experiences", tags=["experiences"])


@router.get("", response_model=ApiResponse[list[ExperiencePublic]])
def list_experiences(
    service: ExperienceService = Depends(get_experience_service),
) -> ApiResponse[list[ExperiencePublic]]:
    experiences = service.list_experiences(published_only=True)
    return success_response(experiences, message="Experiencias obtenidas correctamente")


@router.get("/{experience_id}", response_model=ApiResponse[ExperiencePublic])
def get_experience(
    experience_id: int,
    service: ExperienceService = Depends(get_experience_service),
) -> ApiResponse[ExperiencePublic]:
    experience = service.get_public_experience(experience_id)
    return success_response(experience, message="Experiencia obtenida correctamente")


@router.post("", response_model=ApiResponse[ExperienceRead], status_code=status.HTTP_201_CREATED)
def create_experience(
    payload: ExperienceCreate,
    service: ExperienceService = Depends(get_experience_service),
) -> ApiResponse[ExperienceRead]:
    experience = service.create_experience(payload)
    return success_response(experience, message="Experiencia creada correctamente")


@router.put("/{experience_id}", response_model=ApiResponse[ExperienceRead])
def update_experience(
    experience_id: int,
    payload: ExperienceUpdate,
    service: ExperienceService = Depends(get_experience_service),
) -> ApiResponse[ExperienceRead]:
    experience = service.update_experience(experience_id, payload)
    return success_response(experience, message="Experiencia actualizada correctamente")


@router.delete("/{experience_id}", response_model=ApiResponse[None])
def delete_experience(
    experience_id: int,
    service: ExperienceService = Depends(get_experience_service),
) -> ApiResponse[None]:
    service.delete_experience(experience_id)
    return success_response(None, message="Experiencia eliminada correctamente")
