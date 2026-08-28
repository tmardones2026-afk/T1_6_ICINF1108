from fastapi import APIRouter, status
from app.shared.api_response import ApiResponse
from app.pets.pets_service import pets_service
from app.pets.pets_schemas import CreatePetDto, UpdatePetDto

router = APIRouter(prefix="/api/students", tags=["Pets"])

@router.get("/{student_id}/pets")
def find_all_for_student(student_id: str):
    pets = pets_service.find_all_for_student(student_id)
    return ApiResponse.ok(
        data=pets,
        message="Mascotas obtenidas exitosamente",
        status_code=status.HTTP_200_OK
    )

@router.post("/{student_id}/pets", status_code=status.HTTP_201_CREATED)
def create(student_id: str, data: CreatePetDto):
    new_pet = pets_service.create(student_id, data)
    return ApiResponse.ok(
        data=new_pet,
        message="Mascota creada exitosamente",
        status_code=status.HTTP_201_CREATED
    )

@router.put("/{student_id}/pets/{pet_id}")
def update(student_id: str, pet_id: str, data: UpdatePetDto):
    updated_pet = pets_service.update(student_id, pet_id, data)
    return ApiResponse.ok(
        data=updated_pet,
        message="Mascota actualizada exitosamente",
        status_code=status.HTTP_200_OK
    )

@router.delete("/{student_id}/pets/{pet_id}")
def delete(student_id: str, pet_id: str):
    deleted_pet = pets_service.delete(student_id, pet_id)
    return ApiResponse.ok(
        data=deleted_pet,
        message="Mascota eliminada exitosamente",
        status_code=status.HTTP_200_OK
    )