import pytest
from app.database.connection import Base, engine, SessionLocal
from app.database.models import Complaint
from app.services.trend_service import calculate_category_trends, detect_temporal_anomalies


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    c1 = Complaint(complaint_id="RAI-T01", complaint_text="AC failure in coach B4.", complaint_type="Air Conditioning")
    db.add(c1)
    db.commit()
    yield
    db.close()


def test_calculate_category_trends():
    db = SessionLocal()
    trends = calculate_category_trends(db)
    assert isinstance(trends, list)
    assert len(trends) >= 1
    assert "trend" in trends[0]
    db.close()
