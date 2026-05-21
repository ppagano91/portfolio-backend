from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.schemas.common import ApiResponse, ErrorDetail


class AppError(Exception):
    def __init__(self, message: str, code: str, status_code: int, detail: str | None = None):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.detail = detail or message
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, resource: str, identifier: str | int | None = None):
        detail = f"{resource} no encontrado"
        if identifier is not None:
            detail = f"{resource} '{identifier}' no encontrado"
        super().__init__(
            message=detail,
            code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class ConflictError(AppError):
    def __init__(self, message: str, code: str = "CONFLICT"):
        super().__init__(
            message=message,
            code=code,
            status_code=status.HTTP_409_CONFLICT,
            detail=message,
        )


class BadRequestError(AppError):
    def __init__(self, message: str, code: str = "BAD_REQUEST"):
        super().__init__(
            message=message,
            code=code,
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )


def _error_response(
    message: str,
    code: str,
    detail: str,
    status_code: int,
) -> JSONResponse:
    body = ApiResponse[None](
        success=False,
        data=None,
        message=message,
        error=ErrorDetail(code=code, detail=detail),
    )
    return JSONResponse(status_code=status_code, content=body.model_dump())


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
        return _error_response(
            message=exc.message,
            code=exc.code,
            detail=exc.detail,
            status_code=exc.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        detail = "; ".join(
            f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}"
            for err in exc.errors()
        )
        return _error_response(
            message="Error de validación en la solicitud",
            code="VALIDATION_ERROR",
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_handler(
        _request: Request, exc: ValidationError
    ) -> JSONResponse:
        return _error_response(
            message="Error de validación",
            code="VALIDATION_ERROR",
            detail=str(exc),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        _request: Request, exc: Exception
    ) -> JSONResponse:
        return _error_response(
            message="Error al procesar la solicitud",
            code="INTERNAL_ERROR",
            detail=str(exc),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
