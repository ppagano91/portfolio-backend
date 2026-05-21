from fastapi import APIRouter, Depends, status

from app.api.deps import get_dashboard_service
from app.schemas.common import ApiResponse, success_response
from app.schemas.dashboard import DashboardCreate, DashboardRead
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboards", tags=["dashboards"])


@router.get("", response_model=ApiResponse[list[DashboardRead]])
def list_dashboards(
    service: DashboardService = Depends(get_dashboard_service),
) -> ApiResponse[list[DashboardRead]]:
    dashboards = service.list_dashboards()
    return success_response(dashboards)


@router.get("/{dashboard_id}", response_model=ApiResponse[DashboardRead])
def get_dashboard(
    dashboard_id: int,
    service: DashboardService = Depends(get_dashboard_service),
) -> ApiResponse[DashboardRead]:
    dashboard = service.get_by_id(dashboard_id)
    return success_response(dashboard)


@router.post("", response_model=ApiResponse[DashboardRead], status_code=status.HTTP_201_CREATED)
def create_dashboard(
    payload: DashboardCreate,
    service: DashboardService = Depends(get_dashboard_service),
) -> ApiResponse[DashboardRead]:
    dashboard = service.create(payload)
    return success_response(dashboard, message="Dashboard creado correctamente")
