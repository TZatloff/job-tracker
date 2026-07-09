from fastapi.testclient import TestClient
from main import app
from config import API_TOKEN

client = TestClient(app)
AUTH = {"Authorization": f"Bearer {API_TOKEN}"}


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_admin_requires_token():
    response = client.get("/api/v1/admin/stats")
    assert response.status_code == 422

    response = client.get("/api/v1/admin/stats", headers={"Authorization": "Bearer wrongtoken"})
    assert response.status_code == 401


def test_admin_with_token():
    response = client.get("/api/v1/admin/stats", headers=AUTH)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_create_company_validation():
    response = client.post("/api/v1/companies", json={})
    assert response.status_code == 422


def test_application_bad_company():
    response = client.post("/api/v1/applications", json={"company_id": 999, "position": "Engineer"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Company not found"}
