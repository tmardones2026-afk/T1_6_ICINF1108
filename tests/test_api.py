import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crear_sala_y_obtener_en_listado():
    # 1. Crear sala
    payload = {
        "name": "Sala de Estudio A",
        "location": "Piso 1",
        "capacity": 6,
        "type": "STUDY_ROOM",
        "equipment": ["Pizarra", "Enchufes"]
    }
    response = client.post("/api/rooms", json=payload)
    assert response.status_code == 201
    res_json = response.json()
    assert res_json["success"] is True
    room_id = res_json["data"]["id"]

    # 2. Verificar que aparece en el listado (Criterio P7)
    get_response = client.get("/api/rooms")
    assert get_response.status_code == 200
    rooms = get_response.json()["data"]
    assert any(r["id"] == room_id for r in rooms)

def test_reserva_duplicada_devuelve_409():
    # Crear sala de prueba
    room_resp = client.post("/api/rooms", json={
        "name": "Lab B", "location": "Piso 2", "capacity": 10, "type": "LAB", "equipment": []
    })
    room_id = room_resp.json()["data"]["id"]

    # Reserva 1
    res1 = client.post("/api/reservations", json={
        "roomId": room_id, "userId": "usr1", "date": "2026-11-01", "startTime": "09:00", "endTime": "11:00"
    })
    assert res1.status_code == 201

    # Reserva 2 (Mismo horario / traslape -> Criterio P7)
    res2 = client.post("/api/reservations", json={
        "roomId": room_id, "userId": "usr2", "date": "2026-11-01", "startTime": "10:00", "endTime": "12:00"
    })
    assert res2.status_code == 409
    assert res2.json()["success"] is False

def test_filtrado_orden_y_paginacion():
    # Criterio P7: GET con filtro + orden + paginación
    response = client.get("/api/reservations?sort=date&page=1&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["success"] is True