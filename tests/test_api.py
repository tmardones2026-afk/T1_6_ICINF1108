import sys
from pathlib import Path

# Configurar PYTHONPATH
root_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_path))
sys.path.insert(0, str(root_path / "app"))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_endpoint_no_encontrado_devuelve_404_estandarizado():
    """
    Verifica que el interceptor maneje correctamente el error 404
    y devuelva la estructura estándar con 'timestamp'.
    """
    response = client.get("/api/endpoint-inexistente")
    assert response.status_code == 404
    
    data = response.json()
    assert data["success"] is False
    assert data["statusCode"] == 404
    assert "timestamp" in data


def test_crud_estudiantes_en_memoria():
    """
    Prueba funcional de creación y listado sobre /api/students.
    """
    student_payload = {
        "name": "Diego Vásquez",
        "email": "diego.qa@example.com",
        "age": 21
    }
    
    # 1. Crear estudiante
    response_create = client.post("/api/students", json=student_payload)
    assert response_create.status_code in [200, 201]
    assert response_create.json()["success"] is True

    # 2. Listar estudiantes
    response_list = client.get("/api/students")
    assert response_list.status_code == 200
    assert response_list.json()["success"] is True


def test_error_de_validacion_422():
    """
    Prueba que el envío de un objeto inválido retorne HTTP 422.
    """
    payload_invalido = {"age": "no-es-un-numero"}
    response = client.post("/api/students", json=payload_invalido)
    assert response.status_code == 422
    
    data = response.json()
    assert data["success"] is False
    assert data["statusCode"] == 422