# tests/test_patinetes.py

from app.models import Zona, Patinete

# -------------------- TEST 1 -------------------------
def test_crear_zona(client):
    response = client.post("/zonas/", json={
        "nombre": "Centro",
        "codigo_postal": "41001",
        "limite_velocidad": 25
    })

    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Centro"
    assert "id" in data


# -------------------- TEST 2 -------------------------
def test_crear_patinete(client):
    # Crear zona primero
    zona = client.post("/zonas/", json={
        "nombre": "Nervión",
        "codigo_postal": "41005",
        "limite_velocidad": 25
    }).json()

    response = client.post("/patinetes/", json={
        "numero_serie": "ABC123",
        "modelo": "Xiaomi",
        "bateria": 80,
        "estado": "disponible",
        "zona_id": zona["id"]
    })

    assert response.status_code == 200
    data = response.json()
    assert data["zona_id"] == zona["id"]


# -------------------- TEST 3 -------------------------
def test_bateria_invalida(client):
    zona = client.post("/zonas/", json={
        "nombre": "Centro",
        "codigo_postal": "41001",
        "limite_velocidad": 25
    }).json()

    response = client.post("/patinetes/", json={
        "numero_serie": "ABC999",
        "modelo": "Xiaomi",
        "bateria": 150,
        "estado": "disponible",
        "zona_id": zona["id"]
    })

    assert response.status_code == 422


# -------------------- TEST 4 -------------------------
def test_mantenimiento(client):
    zona = client.post("/zonas/", json={
        "nombre": "Centro",
        "codigo_postal": "41001",
        "limite_velocidad": 25
    }).json()

    # Patinetes
    client.post("/patinetes/", json={
        "numero_serie": "LOW1",
        "modelo": "Xiaomi",
        "bateria": 10,
        "estado": "disponible",
        "zona_id": zona["id"]
    })

    client.post("/patinetes/", json={
        "numero_serie": "HIGH1",
        "modelo": "Xiaomi",
        "bateria": 80,
        "estado": "disponible",
        "zona_id": zona["id"]
    })

    response = client.post(f"/zonas/{zona['id']}/mantenimiento")

    assert response.status_code == 200
    data = response.json()
    assert data["cantidad"] == 1


# -------------------- TEST 5 -------------------------
def test_estado_cambia_a_mantenimiento(client):
    zona = client.post("/zonas/", json={
        "nombre": "Centro",
        "codigo_postal": "41001",
        "limite_velocidad": 25
    }).json()

    patinete = client.post("/patinetes/", json={
        "numero_serie": "LOW2",
        "modelo": "Xiaomi",
        "bateria": 5,
        "estado": "disponible",
        "zona_id": zona["id"]
    }).json()

    client.post(f"/zonas/{zona['id']}/mantenimiento")

    # Endpoint GET /patinetes/{id} debe existir
    response = client.get(f"/patinetes/{patinete['id']}")

    assert response.status_code == 200
    assert response.json()["estado"] == "mantenimiento"