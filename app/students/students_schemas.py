from typing import List, Optional
from pydantic import BaseModel
from app.shared.response_schema import ApiResponse  # Importa tuApiResponse generico

# --- Esquema base del estudiante ---
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class StudentCreate(StudentBase):
    pass

class StudentRead(StudentBase):
    id: int

    class Config:
        from_attributes = True

# --- Esquemas estandarizados envueltos con ApiResponse ---
# Respuesta para un solo estudiante (GET /students/{id}, POST, PUT)
class SingleStudentResponse(ApiResponse[StudentRead]):
    pass

# Respuesta para una lista de estudiantes (GET /students)
class ListStudentResponse(ApiResponse[List[StudentRead]]):
    pass