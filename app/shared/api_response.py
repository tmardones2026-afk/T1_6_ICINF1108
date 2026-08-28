from typing import Any
from datetime import datetime, timezone
from pydantic import BaseModel


class ApiResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: Any = None
    timestamp: str = None

    @classmethod
    def ok(cls, data: Any = None, message: str = "OK", status_code: int = 200):
        return cls(
            success=True,
            statusCode=status_code,
            message=message,
            data=data,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    @classmethod
    def error(cls, message: str = "Error", status_code: int = 400):
        return cls(
            success=False,
            statusCode=status_code,
            message=message,
            data=None,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )