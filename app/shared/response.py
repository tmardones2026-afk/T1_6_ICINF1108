from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorDetail(BaseModel):
    type: str
    details: str


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    status_code: int
    message: str
    data: Optional[T] = None
    error: Optional[ErrorDetail] = None

    @classmethod
    def ok(
        cls,
        data: T,
        message: str = "OK",
        status_code: int = 200,
    ) -> "ApiResponse[T]":
        return cls(
            success=True,
            status_code=status_code,
            message=message,
            data=data,
            error=None,
        )

    @classmethod
    def fail(
        cls,
        message: str,
        status_code: int,
        error_type: str,
        details: str,
    ) -> "ApiResponse[None]":
        return cls(
            success=False,
            status_code=status_code,
            message=message,
            data=None,
            error=ErrorDetail(type=error_type, details=details),
        )