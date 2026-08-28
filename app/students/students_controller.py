from fastapi import APIRouter

from app.pets.pets_service import pets_service
from app.shared.response import ApiResponse
from app.students.students_schemas import CreateStudentDto, Student, UpdateStudentDto
from app.students.students_service import students_service

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.get("", response_model=ApiResponse[Student])
def find_all() -> ApiResponse[Student]:
    students = students_service.find_all()
    return ApiResponse.ok(data=students, message="Estudiantes obtenidos correctamente")


@router.get("/{student_id}", response_model=ApiResponse[Student])
def find_by_id(student_id: str) -> ApiResponse[Student]:
    student = students_service.find_by_id(student_id)
    return ApiResponse.ok(data=student, message="Estudiante obtenido correctamente")


@router.post("", status_code=201, response_model=ApiResponse[Student])
def create(body: CreateStudentDto) -> ApiResponse[Student]:
    student = students_service.create(body)
    return ApiResponse.ok(data=student, message="Estudiante creado correctamente", status_code=201)


@router.patch("/{student_id}", response_model=ApiResponse[Student])
def update(student_id: str, body: UpdateStudentDto) -> ApiResponse[Student]:
    student = students_service.update(student_id, body)
    return ApiResponse.ok(data=student, message="Estudiante actualizado correctamente")


@router.delete("/{student_id}", response_model=ApiResponse[Student])
def delete(student_id: str) -> ApiResponse[Student]:
    deleted = students_service.delete(student_id)
    pets_service.delete_all_for_student(student_id)

    return ApiResponse.ok(data=deleted, message="Estudiante eliminado correctamente")