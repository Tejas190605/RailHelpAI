import pytest
from app.database.connection import Base, engine, SessionLocal
from app.database.models import Complaint
from app.services.recommendation_engine import generate_operational_recommendations
from app.services.risk_service import calculate_operational_risk_index


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    c1 = Complaint(complaint_id="RAI-R01", complaint_text="Medical emergency on train 12951.", priority="P1", complaint_type="Medical")
    db.add(c1)
    db.commit()
    yield
    db.close()


def test_generate_operational_recommendations():
    db = SessionLocal()
    recs = generate_operational_recommendations(db)
    assert isinstance(recs, list)
    db.close()


def test_calculate_operational_risk_index():
    db = SessionLocal()
    risk = calculate_operational_risk_index(db)
    assert risk["risk_index"] >= 0.0
    assert "risk_level" in risk
    assert "disclaimer" in risk
    db.close()
