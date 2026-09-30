from datetime import datetime, timezone
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Importar respuestas compartidas
try:
    from app.shared.api_response import ApiResponse
except ModuleNotFoundError:
    from shared.api_response import ApiResponse

# Importar controladores de estudiantes y mascotas
try:
    from app.students.students_controller import router as students_router
    from app.pets.pets_controller import router as pets_router
except ModuleNotFoundError:
    from students.students_controller import router as students_router
    from pets.pets_controller import router as pets_router

app = FastAPI(title="Students & Pets API")

# Incluir las rutas en la aplicación
app.include_router(students_router, prefix="/api/students", tags=["Students"])
app.include_router(pets_router, prefix="/api/students", tags=["Pets"])


# Intercepta excepciones HTTP (404, 401, 403, 409, 500, etc.)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    response_body = ApiResponse(
        success=False,
        statusCode=exc.status_code,
        message=str(exc.detail),
        data=None,
        timestamp=datetime.now(timezone.utc).isoformat()
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response_body.model_dump()
    )


# Intercepta errores de validación de Pydantic (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    response_body = ApiResponse(
        success=False,
        statusCode=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Error de validación en la petición",
        data=None,
        timestamp=datetime.now(timezone.utc).isoformat()
    )
    payload = response_body.model_dump()
    payload["errors"] = exc.errors()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=payload
    )