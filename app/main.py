from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas import ApiResponse

app = FastAPI()

# Intercepta excepciones HTTP (404, 401, 403, 500, etc.)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    response_body = ApiResponse.error_response(
        message=str(exc.detail),
        status_code=exc.status_code
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response_body.model_dump()
    )

# Intercepta errores de validación de Pydantic (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    response_body = ApiResponse.error_response(
        message="Error de validación en la petición",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
    # Si quieres incluir detalles de los campos con error:
    payload = response_body.model_dump()
    payload["errors"] = exc.errors()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=payload
    )