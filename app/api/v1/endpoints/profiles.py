from fastapi import APIRouter, Depends, status

from app.api.deps import get_profile_service
from app.schemas.common import ApiResponse, success_response
from app.schemas.profile import ProfileCreate, ProfilePublic, ProfileRead, ProfileUpdate
from app.services.profile_service import ProfileService

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/{slug}", response_model=ApiResponse[ProfilePublic])
def get_profile_by_slug(
    slug: str,
    service: ProfileService = Depends(get_profile_service),
) -> ApiResponse[ProfilePublic]:
    profile = service.get_profile_by_slug(slug)
    return success_response(profile, message="Perfil obtenido correctamente")


@router.post("", response_model=ApiResponse[ProfileRead], status_code=status.HTTP_201_CREATED)
def create_profile(
    payload: ProfileCreate,
    service: ProfileService = Depends(get_profile_service),
) -> ApiResponse[ProfileRead]:
    profile = service.create_profile(payload)
    return success_response(profile, message="Perfil creado correctamente")


@router.put("/{profile_id}", response_model=ApiResponse[ProfileRead])
def update_profile(
    profile_id: int,
    payload: ProfileUpdate,
    service: ProfileService = Depends(get_profile_service),
) -> ApiResponse[ProfileRead]:
    profile = service.update_profile(profile_id, payload)
    return success_response(profile, message="Perfil actualizado correctamente")


@router.delete("/{profile_id}", response_model=ApiResponse[None])
def delete_profile(
    profile_id: int,
    service: ProfileService = Depends(get_profile_service),
) -> ApiResponse[None]:
    service.delete_profile(profile_id)
    return success_response(None, message="Perfil eliminado correctamente")
