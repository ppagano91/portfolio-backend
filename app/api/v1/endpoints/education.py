from fastapi import APIRouter, Depends, status

from app.api.deps import get_education_service
from app.schemas.common import ApiResponse, success_response
from app.schemas.education import (
    EducationCreate,
    EducationPublic,
    EducationRead,
    EducationUpdate,
)
from app.services.education_service import EducationService

router = APIRouter(prefix="/education", tags=["education"])


@router.get("", response_model=ApiResponse[list[EducationPublic]])
def list_education(
    service: EducationService = Depends(get_education_service),
) -> ApiResponse[list[EducationPublic]]:
    education = service.list_education(published_only=True)
    return success_response(education, message="Educación obtenida correctamente")


@router.get("/{education_id}", response_model=ApiResponse[EducationPublic])
def get_education(
    education_id: int,
    service: EducationService = Depends(get_education_service),
) -> ApiResponse[EducationPublic]:
    record = service.get_public_education(education_id)
    return success_response(record, message="Registro de educación obtenido correctamente")


@router.post("", response_model=ApiResponse[EducationRead], status_code=status.HTTP_201_CREATED)
def create_education(
    payload: EducationCreate,
    service: EducationService = Depends(get_education_service),
) -> ApiResponse[EducationRead]:
    record = service.create_education(payload)
    return success_response(record, message="Educación creada correctamente")


@router.put("/{education_id}", response_model=ApiResponse[EducationRead])
def update_education(
    education_id: int,
    payload: EducationUpdate,
    service: EducationService = Depends(get_education_service),
) -> ApiResponse[EducationRead]:
    record = service.update_education(education_id, payload)
    return success_response(record, message="Educación actualizada correctamente")


@router.delete("/{education_id}", response_model=ApiResponse[None])
def delete_education(
    education_id: int,
    service: EducationService = Depends(get_education_service),
) -> ApiResponse[None]:
    service.delete_education(education_id)
    return success_response(None, message="Educación eliminada correctamente")
