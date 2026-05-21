from fastapi import APIRouter, Depends, status

from app.api.deps import get_contact_service
from app.schemas.common import ApiResponse, success_response
from app.schemas.contact import ContactCreate, ContactRead
from app.services.contact_service import ContactService

router = APIRouter(prefix="/contact", tags=["contact"])


@router.post("", response_model=ApiResponse[ContactRead], status_code=status.HTTP_201_CREATED)
def send_contact_message(
    payload: ContactCreate,
    service: ContactService = Depends(get_contact_service),
) -> ApiResponse[ContactRead]:
    message = service.create_message(payload)
    return success_response(message, message="Mensaje enviado correctamente")
