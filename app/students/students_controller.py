from fastapi import APIRouter

from app.pets.pets_service import pets_service
from app.shared.api_response import ApiResponse
from app.students.students_schemas import CreateStudentDto, Student, UpdateStudentDto
from app.students.students_service import students_service

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.get("")
def find_all() -> ApiResponse[list[Student]]:
    students = students_service.find_all()
    return ApiResponse.ok(data=students, message="Estudiantes obtenidos")


@router.get("/{student_id}")
def find_by_id(student_id: str) -> ApiResponse[Student]:
    student = students_service.find_by_id(student_id)
    return ApiResponse.ok(data=student, message="Estudiante encontrado")


@router.post("", status_code=201)
def create(body: CreateStudentDto) -> ApiResponse[Student]:
    student = students_service.create(body)
    return ApiResponse.ok(data=student, message="Estudiante creado", status_code=201)


@router.patch("/{student_id}")
def update(student_id: str, body: UpdateStudentDto) -> ApiResponse[Student]:
    student = students_service.update(student_id, body)
    return ApiResponse.ok(data=student, message="Estudiante actualizado")


@router.delete("/{student_id}")
def delete(student_id: str) -> ApiResponse[Student]:
    deleted = students_service.delete(student_id)
    pets_service.delete_all_for_student(student_id)
    return ApiResponse.ok(data=deleted, message="Estudiante eliminado")