from datetime import datetime, timezone
from typing import Generic, Optional, TypeVar, Union

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    statusCode: int
    message: str
    data: Optional[Union[T, list[T]]] = None
    timestamp: str

    @classmethod
    def ok(
        cls,
        data: Optional[Union[T, list[T]]] = None,
        message: str = "OK",
        status_code: int = 200,
    ) -> "ApiResponse[T]":
        return cls(
            success=True,
            statusCode=status_code,
            message=message,
            data=data,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    @classmethod
    def fail(
        cls,
        message: str,
        status_code: int,
        data: Optional[Union[T, list[T]]] = None,
    ) -> "ApiResponse[T]":
        return cls(
            success=False,
            statusCode=status_code,
            message=message,
            data=data,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )