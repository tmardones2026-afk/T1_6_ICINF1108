from fastapi import APIRouter, HTTPException

from app.pets.pets_schemas import CreatePetDto, Pet, UpdatePetDto
from app.pets.pets_service import pets_service

router = APIRouter(
    prefix="/api/students/{studentId}/pets",
    tags=["Pets"],
)


@router.get("")
def find_all(studentId: str):
    pets = pets_service.find_all_for_student(studentId)
    return {
        "success": True,
        "statusCode": 200,
        "message": "Mascotas obtenidas correctamente",
        "data": pets
    }


@router.post("", status_code=201)
def create(studentId: str, body: CreatePetDto):
    pet = pets_service.create(studentId, body)
    return {
        "success": True,
        "statusCode": 201,
        "message": "Mascota creada correctamente",
        "data": pet
    }


@router.patch("/{petId}")
def update(studentId: str, petId: str, body: UpdatePetDto):
    pet = pets_service.update(studentId, petId, body)

    if pet is None:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    return {
        "success": True,
        "statusCode": 200,
        "message": "Mascota actualizada correctamente",
        "data": pet
    }


@router.delete("/{petId}")
def delete(studentId: str, petId: str):
    deleted = pets_service.delete(studentId, petId)

    if deleted is None:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    return {
        "success": True,
        "statusCode": 200,
        "message": "Mascota eliminada correctamente",
        "data": deleted
    }