from fastapi import APIRouter
from app.pets.pets_schemas import CreatePetDto, UpdatePetDto
from app.pets.pets_service import pets_service
from app.shared.api_response import ApiResponse

router = APIRouter(
    prefix="/api/students/{studentId}/pets",
    tags=["Pets"],
)

@router.get("")
def find_all(studentId: str):
    pets = pets_service.find_all_for_student(studentId)
    return ApiResponse.ok(
        data=pets, 
        message="Mascotas obtenidas exitosamente"
    )

@router.post("", status_code=201)
def create(studentId: str, body: CreatePetDto):
    new_pet = pets_service.create(studentId, body)
    return ApiResponse.ok(
        data=new_pet, 
        message="Mascota creada exitosamente", 
        status_code=201
    )

@router.patch("/{petId}")
def update(studentId: str, petId: str, body: UpdatePetDto):
    updated_pet = pets_service.update(studentId, petId, body)
    if not updated_pet:
        return ApiResponse.error(
            message=f"No se encontró la mascota con ID {petId}", 
            status_code=404
        )
    return ApiResponse.ok(
        data=updated_pet, 
        message="Mascota actualizada exitosamente"
    )

@router.delete("/{petId}")
def delete(studentId: str, petId: str):
    deleted_pet = pets_service.delete(studentId, petId)
    if not deleted_pet:
        return ApiResponse.error(
            message=f"No se encontró la mascota con ID {petId}", 
            status_code=404
        )
    return ApiResponse.ok(
        data=deleted_pet, 
        message="Mascota eliminada exitosamente"
    )