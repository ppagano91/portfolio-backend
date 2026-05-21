from fastapi import APIRouter, Depends

from app.api.deps import get_profile_service
from app.schemas.common import ApiResponse, success_response
from app.schemas.profile import ProfilePublic
from app.services.profile_service import ProfileService

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=ApiResponse[ProfilePublic])
def get_public_profile(
    service: ProfileService = Depends(get_profile_service),
) -> ApiResponse[ProfilePublic]:
    profile = service.get_public_profile()
    return success_response(profile, message="Perfil obtenido correctamente")
