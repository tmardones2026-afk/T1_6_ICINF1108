from fastapi import APIRouter, status
from app.shared.api_response import ApiResponse
from app.pets.pets_service import pets_service
from app.pets.pets_schemas import CreatePetDto, UpdatePetDto, Pet

router = APIRouter(prefix="/api/students/{studentId}/pets", tags=["Pets"])

@router.get("")
def find_all(studentId: str) -> ApiResponse[list[Pet]]:
    pets = pets_service.find_all_for_student(studentId)
    return ApiResponse.ok(data=pets, message="Mascotas obtenidas")


@router.post("", status_code=201)
def create(studentId: str, body: CreatePetDto) -> ApiResponse[Pet]:
    pet = pets_service.create(studentId, body)
    return ApiResponse.ok(data=pet, message="Mascota creada", status_code=201)


@router.patch("/{petId}")
def update(studentId: str, petId: str, body: UpdatePetDto) -> ApiResponse[Pet]:
    pet = pets_service.update(studentId, petId, body)
    return ApiResponse.ok(data=pet, message="Mascota actualizada")


@router.delete("/{petId}")
def delete(studentId: str, petId: str) -> ApiResponse[Pet]:
    deleted = pets_service.delete(studentId, petId)
    return ApiResponse.ok(data=deleted, message="Mascota eliminada")
