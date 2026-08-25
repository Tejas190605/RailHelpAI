import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import Base, engine, SessionLocal
from app.database.models import Complaint

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    c1 = Complaint(complaint_id="RAI-INT01", complaint_text="AC is not working in coach B4.", complaint_type="Air Conditioning", train_number="12951", station="Pune")
    db.add(c1)
    db.commit()
    yield
    db.close()


def test_api_detect_duplicates():
    res = client.post("/api/v1/ai/detect-duplicates", json={"text": "AC broken in coach B4."})
    assert res.status_code == 200
    data = res.json()
    assert "is_duplicate" in data


def test_api_predict_resolution():
    res = client.post("/api/v1/ai/predict-resolution", json={"category": "Air Conditioning", "priority": "P2", "department": "Electrical"})
    assert res.status_code == 200
    data = res.json()
    assert data["predicted_resolution_minutes"] > 0


def test_api_clusters():
    res = client.get("/api/v1/analytics/clusters")
    assert res.status_code == 200


def test_api_hotspots():
    res = client.get("/api/v1/analytics/hotspots")
    assert res.status_code == 200


def test_api_train_profile():
    res = client.get("/api/v1/analytics/trains/12951")
    assert res.status_code == 200
    data = res.json()
    assert data["train_number"] == "12951"


def test_api_station_profile():
    res = client.get("/api/v1/analytics/stations/Pune")
    assert res.status_code == 200
    data = res.json()
    assert data["station_name"] == "Pune"
