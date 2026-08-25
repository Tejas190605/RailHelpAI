import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import Base, engine, SessionLocal
from app.database.models import Complaint

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Ensure clean database schema before each test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def test_health_check():
    """Verify health endpoint returns 200 OK and healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data


def test_create_complaint():
    """Verify creating a complaint via POST /api/v1/complaints."""
    payload = {
        "complaint_text": "AC is not cooling in coach B4 seat 21 since Pune.",
        "train_number": "12951",
        "coach": "B4",
        "seat": "21",
        "station": "Pune"
    }
    response = client.post("/api/v1/complaints", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["complaint_id"].startswith("RAI-")
    assert data["complaint_text"] == payload["complaint_text"]
    assert data["status"] in ["New", "PENDING_REVIEW", "ASSIGNED"]


def test_list_complaints():
    """Verify retrieving complaints list via GET /api/v1/complaints."""
    response = client.get("/api/v1/complaints")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data
    assert isinstance(data["items"], list)


def test_get_complaint_by_id():
    """Verify retrieving complaint detail by reference ID."""
    # First create a complaint
    payload = {"complaint_text": "Water leakage in coach S2 toilet."}
    create_res = client.post("/api/v1/complaints", json=payload)
    complaint_id = create_res.json()["complaint_id"]

    # Retrieve created complaint
    response = client.get(f"/api/v1/complaints/{complaint_id}")
    assert response.status_code == 200
    assert response.json()["complaint_id"] == complaint_id


def test_update_complaint_status():
    """Verify updating status via PATCH /api/v1/complaints/{id}/status."""
    create_res = client.post("/api/v1/complaints", json={"complaint_text": "Dirty seat in coach A1."})
    complaint_id = create_res.json()["complaint_id"]

    patch_res = client.patch(
        f"/api/v1/complaints/{complaint_id}/status",
        json={"status": "In Progress"}
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "In Progress"


def test_delete_complaint():
    """Verify deleting complaint via DELETE /api/v1/complaints/{id}."""
    create_res = client.post("/api/v1/complaints", json={"complaint_text": "Broken window lock."})
    complaint_id = create_res.json()["complaint_id"]

    del_res = client.delete(f"/api/v1/complaints/{complaint_id}")
    assert del_res.status_code == 204

    # Verify 404 on subsequent get
    get_res = client.get(f"/api/v1/complaints/{complaint_id}")
    assert get_res.status_code == 404
