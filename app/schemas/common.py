from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str
    detail: str


class ApiResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(from_attributes=True)

    success: bool
    data: T | None = None
    message: str
    error: ErrorDetail | None = None


def success_response(
    data: T,
    message: str = "Operación realizada correctamente",
) -> ApiResponse[T]:
    return ApiResponse(success=True, data=data, message=message, error=None)
