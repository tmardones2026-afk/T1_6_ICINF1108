from datetime import datetime, timezone
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    statusCode: int
    message: str
    data: T | None
    timestamp: str

    @classmethod
    def ok(cls, data: T, message: str = "OK", status_code: int = 200) -> "ApiResponse[T]":
        return cls(
            success=True,
            statusCode=status_code,
            message=message,
            data=data,
            timestamp=_now_iso(),
        )

    @classmethod
    def error(cls, message: str, status_code: int) -> "ApiResponse[None]":
        return cls(
            success=False,
            statusCode=status_code,
            message=message,
            data=None,
            timestamp=_now_iso(),
        )


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")