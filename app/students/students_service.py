from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException, status

from app.shared.in_memory_store import InMemoryStore
from app.shared.response_schema import ApiResponse
from app.students.students_schemas import CreateStudentDto, Student, UpdateStudentDto


class StudentsService:
    def __init__(self) -> None:
        self.store: InMemoryStore[Student] = InMemoryStore()

    def find_all(self) -> ApiResponse[list[Student]]:
        students = sorted(self.store.find_all(), key=lambda s: s.createdAt, reverse=True)
        return ApiResponse(
            success=True,
            status_code=status.HTTP_200_OK,
            message="Lista de estudiantes obtenida exitosamente",
            data=students,
        )

    def find_by_id(self, student_id: str) -> ApiResponse[Student]:
        student = self.store.get(student_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estudiante no encontrado",
            )

        return ApiResponse(
            success=True,
            status_code=status.HTTP_200_OK,
            message="Estudiante encontrado exitosamente",
            data=student,
        )

    def create(self, data: CreateStudentDto) -> ApiResponse[Student]:
        self.assert_email_available(data.email)

        now = datetime.now()
        student = Student(
            id=str(uuid4()),
            name=data.name,
            email=data.email,
            age=data.age,
            createdAt=now,
            updatedAt=now,
        )

        self.store.set(student)
        return ApiResponse(
            success=True,
            status_code=status.HTTP_201_CREATED,
            message="Estudiante creado exitosamente",
            data=student,
        )

    def update(self, student_id: str, data: UpdateStudentDto) -> ApiResponse[Student]:
        # Para obtener el estudiante existente se extrae el objeto .data de la respuesta de find_by_id
        existing_res = self.find_by_id(student_id)
        existing = existing_res.data

        if data.email and data.email != existing.email:
            self.assert_email_available(data.email)

        updated = existing.model_copy(
            update={
                **data.model_dump(exclude_none=True),
                "updatedAt": datetime.now(),
            }
        )

        self.store.set(updated)
        return ApiResponse(
            success=True,
            status_code=status.HTTP_200_OK,
            message="Estudiante actualizado exitosamente",
            data=updated,
        )

    def delete(self, student_id: str) -> ApiResponse[Student]:
        existing_res = self.find_by_id(student_id)
        existing = existing_res.data
        self.store.delete(student_id)

        return ApiResponse(
            success=True,
            status_code=status.HTTP_200_OK,
            message="Estudiante eliminado exitosamente",
            data=existing,
        )

    def assert_email_available(self, email: str) -> None:
        exists = any(student.email == email for student in self.store.find_all())

        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El correo electrónico ya está en uso",
            )


students_service = StudentsService()