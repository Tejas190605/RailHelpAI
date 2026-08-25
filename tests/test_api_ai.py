import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_api_ai_analyze():
    payload = {
        "text": "Toilet in coach S3 is extremely dirty and water tap is leaking continuously since Pune.",
        "train_number": "12137"
    }
    response = client.post("/api/v1/ai/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "category" in data
    assert "entities" in data
    assert "priority" in data
    assert "department" in data
    assert data["category"]["value"] in ["Cleanliness", "Water Supply"]


def test_api_ai_classify():
    payload = {"text": "AC is not cooling in coach B4"}
    response = client.post("/api/v1/ai/classify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "Air Conditioning"


def test_api_ai_extract_entities():
    payload = {"text": "Coach B4 seat 21 train 12951"}
    response = client.post("/api/v1/ai/extract-entities", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data.get("coach") == "B4"
    assert data.get("train_number") == "12951"


def test_api_ai_analyze_invalid_input():
    response = client.post("/api/v1/ai/analyze", json={"text": "a"})
    assert response.status_code in [400, 422]
