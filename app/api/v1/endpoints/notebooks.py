from fastapi import APIRouter, Depends, status

from app.api.deps import get_notebook_service
from app.schemas.common import ApiResponse, success_response
from app.schemas.notebook import NotebookCreate, NotebookRead
from app.services.notebook_service import NotebookService

router = APIRouter(prefix="/notebooks", tags=["notebooks"])


@router.get("", response_model=ApiResponse[list[NotebookRead]])
def list_notebooks(
    service: NotebookService = Depends(get_notebook_service),
) -> ApiResponse[list[NotebookRead]]:
    notebooks = service.list_notebooks()
    return success_response(notebooks)


@router.get("/{notebook_id}", response_model=ApiResponse[NotebookRead])
def get_notebook(
    notebook_id: int,
    service: NotebookService = Depends(get_notebook_service),
) -> ApiResponse[NotebookRead]:
    notebook = service.get_by_id(notebook_id)
    return success_response(notebook)


@router.post("", response_model=ApiResponse[NotebookRead], status_code=status.HTTP_201_CREATED)
def create_notebook(
    payload: NotebookCreate,
    service: NotebookService = Depends(get_notebook_service),
) -> ApiResponse[NotebookRead]:
    notebook = service.create(payload)
    return success_response(notebook, message="Notebook creado correctamente")
