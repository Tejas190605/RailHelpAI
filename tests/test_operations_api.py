import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import Base, engine

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def test_operations_assign():
    create_res = client.post("/api/v1/complaints", json={"complaint_text": "Fan is not working in coach S2."})
    c_id = create_res.json()["complaint_id"]

    assign_res = client.post(
        f"/api/v1/complaints/{c_id}/assign",
        json={"department": "Electrical Maintenance", "assigned_to": "Technician Vijay"}
    )
    assert assign_res.status_code == 200
    data = assign_res.json()
    assert data["department"] == "Electrical Maintenance"
    assert data["status"] == "ASSIGNED"


def test_operations_review_ai():
    create_res = client.post("/api/v1/complaints", json={"complaint_text": "Unclean seat berth 41 in coach B3."})
    c_id = create_res.json()["complaint_id"]

    review_res = client.post(
        f"/api/v1/complaints/{c_id}/review",
        json={
            "reviewer": "Supervisor Admin",
            "action": "Override",
            "final_category": "Cleanliness",
            "final_priority": "P2",
            "final_department": "Housekeeping / Sanitation",
            "reason": "Escalated priority due to upcoming inspection."
        }
    )
    assert review_res.status_code == 200
    data = review_res.json()
    assert data["complaint_type"] == "Cleanliness"
    assert data["priority"] == "P2"
    assert data["department"] == "Housekeeping / Sanitation"


def test_operations_resolve():
    create_res = client.post("/api/v1/complaints", json={"complaint_text": "Tap leaking in coach S4."})
    c_id = create_res.json()["complaint_id"]

    resolve_res = client.post(
        f"/api/v1/complaints/{c_id}/resolve",
        json={"resolution_text": "Replaced washer in tap.", "resolution_type": "FIXED"}
    )
    assert resolve_res.status_code == 200
    data = resolve_res.json()
    assert data["status"] == "RESOLVED"
    assert data["resolved_at"] is not None


def test_operations_feedback():
    create_res = client.post("/api/v1/complaints", json={"complaint_text": "Dirty floor in coach A2."})
    c_id = create_res.json()["complaint_id"]

    fb_res = client.post(
        f"/api/v1/complaints/{c_id}/feedback",
        json={"rating": 5, "feedback": "Great service!"}
    )
    assert fb_res.status_code == 200
    data = fb_res.json()
    assert data["rating"] == 5
