import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_invalid_complaint_creation_validation():
    """Verify HTTP 422 Unprocessable Entity for invalid or empty complaint payload."""
    invalid_payload = {
        "complaint_text": ""  # Invalid empty description
    }
    response = client.post("/api/v1/complaints", json=invalid_payload)
    assert response.status_code == 422


def test_nonexistent_complaint_retrieval():
    """Verify HTTP 404 Not Found for non-existent complaint ID."""
    response = client.get("/api/v1/complaints/999999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_ai_analyze_multilingual_hinglish_input():
    """Verify AI analysis handles Hinglish inputs with preserved entity extraction."""
    hinglish_text = "AC chal nahi raha hai in coach S3 seat 45 train 12951 near Mumbai"
    response = client.post(
        "/api/v1/ai/analyze",
        json={"text": hinglish_text}
    )
    assert response.status_code == 200
    data = response.json()
    assert "category" in data
    assert "entities" in data
    assert data["entities"].get("coach") == "S3"
    assert data["entities"].get("seat") == "45"


def test_duplicate_detection_schema():
    """Verify duplicate detection endpoint schema and deterministic structure."""
    response = client.post(
        "/api/v1/ai/detect-duplicates",
        json={"text": "AC is not cooling in coach B4 seat 21 on train 12951 since Pune."}
    )
    assert response.status_code == 200
    data = response.json()
    assert "is_duplicate" in data
    assert "similarity_score" in data
    assert isinstance(data["is_duplicate"], bool)
    assert 0.0 <= data["similarity_score"] <= 1.0


def test_resolution_prediction_schema():
    """Verify resolution prediction endpoint returns non-negative numeric duration."""
    response = client.post(
        "/api/v1/ai/predict-resolution",
        json={"category": "Air Conditioning", "priority": "P2"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "predicted_resolution_minutes" in data
    assert data["predicted_resolution_minutes"] >= 0.0
