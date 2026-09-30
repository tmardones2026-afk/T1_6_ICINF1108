from datetime import datetime, timezone
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.shared.api_response import ApiResponse
from app.students.students_controller import router as students_router
from app.pets.pets_controller import router as pets_router

app = FastAPI(title="Students & Pets API")

app.include_router(students_router)
app.include_router(pets_router)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    response_body = ApiResponse(
        success=False,
        statusCode=exc.status_code,
        message=str(exc.detail),
        data=None
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response_body.model_dump()
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    response_body = ApiResponse(
        success=False,
        statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Error de validación en la petición",
        data=None
    )
    payload = response_body.model_dump()
    payload["errors"] = exc.errors()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=payload
    )