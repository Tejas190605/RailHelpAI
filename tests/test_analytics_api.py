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


def test_analytics_overview():
    res = client.get("/api/v1/analytics/overview")
    assert res.status_code == 200
    data = res.json()
    assert "total_complaints" in data
    assert "open_complaints" in data
    assert "resolved_complaints" in data
    assert "sla_breaches" in data
    assert "ai_automation_rate" in data
    assert "sla_compliance_rate" in data


def test_analytics_categories():
    res = client.get("/api/v1/analytics/categories")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)


def test_analytics_priority():
    res = client.get("/api/v1/analytics/priority")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)


def test_analytics_departments():
    res = client.get("/api/v1/analytics/departments")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)


def test_analytics_sla():
    res = client.get("/api/v1/analytics/sla")
    assert res.status_code == 200
    data = res.json()
    assert "WITHIN_SLA" in data
    assert "BREACHED" in data
