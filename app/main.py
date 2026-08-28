from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.pets.pets_controller import router as pets_router
from app.shared.api_response import ApiResponse
from app.students.students_controller import router as students_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI CRUD Students & Pets",
        description=(
            "API de un CRUD en memoria para la entidad Student y sus mascotas (Pet)"
        ),
        version="1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        body = ApiResponse.error(message=str(exc.detail), status_code=exc.status_code)
        return JSONResponse(status_code=exc.status_code, content=body.model_dump())

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        body = ApiResponse.error(message="Datos inválidos", status_code=422)
        return JSONResponse(status_code=422, content=body.model_dump())

    app.include_router(students_router)
    app.include_router(pets_router)

    return app


app = create_app()