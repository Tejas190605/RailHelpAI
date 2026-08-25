import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)


def test_request_id_middleware_generated():
    res = client.get("/health/live")
    assert res.status_code == 200
    assert "X-Request-ID" in res.headers
    assert len(res.headers["X-Request-ID"]) > 0


def test_request_id_middleware_reused():
    custom_id = "custom-req-id-12345"
    res = client.get("/health/live", headers={"X-Request-ID": custom_id})
    assert res.status_code == 200
    assert res.headers["X-Request-ID"] == custom_id


def test_health_live_endpoint():
    res = client.get("/health/live")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["app_name"] == settings.APP_NAME


def test_health_ready_endpoint():
    res = client.get("/health/ready")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ready"
    assert data["components"]["database"] == "connected"


def test_global_exception_handler():
    # Force 404/validation endpoint check
    res = client.get("/api/v1/complaints/non-existent-invalid-id-999999")
    assert res.status_code == 404
