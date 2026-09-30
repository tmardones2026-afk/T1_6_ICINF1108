from fastapi import APIRouter

from app.pets.pets_service import pets_service
from app.shared.api_response import ApiResponse
from app.students.students_schemas import CreateStudentDto, Student, UpdateStudentDto
from app.students.students_service import students_service

router = APIRouter(prefix="/api/students", tags=["Students"])

@router.get("")
def find_all() -> ApiResponse[list[Student]]:
    result = students_service.find_all()
    # Si el servicio ya retornó un ApiResponse, sacamos su payload interno
    data = result.data if hasattr(result, "data") else result
    return ApiResponse.ok(data=data, message="Estudiantes obtenidos")

@router.get("/{student_id}")
def find_by_id(student_id: str) -> ApiResponse[Student]:
    result = students_service.find_by_id(student_id)
    data = result.data if hasattr(result, "data") else result
    return ApiResponse.ok(data=data, message="Estudiante encontrado")

@router.post("", status_code=201)
def create(body: CreateStudentDto) -> ApiResponse[Student]:
    result = students_service.create(body)
    data = result.data if hasattr(result, "data") else result
    return ApiResponse.ok(data=data, message="Estudiante creado", status_code=201)

@router.patch("/{student_id}")
def update(student_id: str, body: UpdateStudentDto) -> ApiResponse[Student]:
    result = students_service.update(student_id, body)
    data = result.data if hasattr(result, "data") else result
    return ApiResponse.ok(data=data, message="Estudiante actualizado")

@router.delete("/{student_id}")
def delete(student_id: str) -> ApiResponse[Student]:
    result = students_service.delete(student_id)
    pets_service.delete_all_for_student(student_id)
    data = result.data if hasattr(result, "data") else result
    return ApiResponse.ok(data=data, message="Estudiante eliminado")