import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_canonical_demo_complaint_workflow():
    """
    End-to-end integration test verifying the canonical README demo workflow:
    Input: 'AC is not cooling in coach B4 seat 21 on train 12951 since Pune.'
    Verifies AI triage, entity extraction, priority evaluation, department routing,
    complaint creation, state transitions, and SLA calculation.
    """
    input_text = "AC is not cooling in coach B4 seat 21 on train 12951 since Pune."
    
    # 1. Run AI Pipeline Analysis Endpoint
    ai_response = client.post(
        "/api/v1/ai/analyze",
        json={"text": input_text}
    )
    assert ai_response.status_code == 200
    ai_data = ai_response.json()
    
    # Assert AI analysis schema and invariants
    assert ai_data["category"]["value"] in ["Air Conditioning", "Electrical"]
    assert ai_data["priority"]["level"] in ["P1", "P2", "P3", "P4"]
    assert 0.0 <= ai_data["category"]["confidence"] <= 1.0
    assert "entities" in ai_data
    
    entities = ai_data["entities"]
    assert entities.get("train_number") == "12951"
    assert entities.get("coach") == "B4"
    assert entities.get("seat") == "21"
    assert entities.get("station") == "Pune"
    
    # 2. Create Complaint in Backend DB via REST API
    create_payload = {
        "complaint_text": input_text,
        "train_number": entities.get("train_number"),
        "coach": entities.get("coach"),
        "seat": entities.get("seat"),
        "station": entities.get("station")
    }
    
    create_response = client.post(
        "/api/v1/complaints",
        json=create_payload
    )
    assert create_response.status_code == 201
    complaint_data = create_response.json()
    
    complaint_id = complaint_data["complaint_id"]
    assert complaint_id is not None
    assert complaint_data["complaint_type"] == ai_data["category"]["value"]
    
    # 3. Verify Complaint Retrieval
    get_response = client.get(f"/api/v1/complaints/{complaint_id}")
    assert get_response.status_code == 200
    assert get_response.json()["complaint_id"] == complaint_id
    
    # 4. Assign Complaint to Department
    assign_response = client.post(
        f"/api/v1/complaints/{complaint_id}/assign",
        json={"department": "Electrical", "assigned_to": "Officer_Kumar"}
    )
    assert assign_response.status_code == 200
    assigned_data = assign_response.json()
    assert assigned_data["status"] == "ASSIGNED"
    
    # 5. Resolve Complaint
    resolve_response = client.post(
        f"/api/v1/complaints/{complaint_id}/resolve",
        json={
            "resolution_text": "Replaced AC capacitor unit in coach B4.",
            "resolution_type": "REPAIRED",
            "resolved_by": "Officer_Kumar"
        }
    )
    assert resolve_response.status_code == 200
    resolved_data = resolve_response.json()
    assert resolved_data["status"] == "RESOLVED"
