from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.schemas.common import ApiResponse, success_response

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", summary="Health check de la aplicación")
def health_check() -> ApiResponse[dict]:
    settings = get_settings()
    data = {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }
    return success_response(data, message="Aplicación en ejecución")


@router.get("/db", summary="Health check de la base de datos")
def health_check_db(db: Session = Depends(get_db)) -> ApiResponse[dict]:
    db.execute(text("SELECT 1"))
    return success_response({"database": "connected"}, message="Base de datos conectada")
