import pytest
from app.database.connection import Base, engine, SessionLocal
from app.database.models import Complaint
from app.services.hotspot_service import get_hotspot_analytics


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    c1 = Complaint(complaint_id="RAI-H01", complaint_text="Medical emergency on train 12951.", train_number="12951", priority="P1")
    c2 = Complaint(complaint_id="RAI-H02", complaint_text="AC failure on train 12951.", train_number="12951", priority="P2")
    db.add_all([c1, c2])
    db.commit()
    yield
    db.close()


def test_get_hotspot_analytics():
    db = SessionLocal()
    hotspots = get_hotspot_analytics(db)
    assert len(hotspots) >= 1
    assert hotspots[0]["identifier"] == "12951"
    assert hotspots[0]["hotspot_score"] > 0
    db.close()
