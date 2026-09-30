from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    statusCode: int
    message: str
    data: Optional[T] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __init__(self, **kwargs):
        # Truco: Si el servicio manda 'status_code', lo convertimos a 'statusCode'
        if "status_code" in kwargs:
            kwargs["statusCode"] = kwargs.pop("status_code")
        super().__init__(**kwargs)

    @classmethod
    def ok(cls, data: Any = None, message: str = "Éxito", status_code: int = 200):
        return cls(
            success=True,
            statusCode=status_code,
            message=message,
            data=data
        )