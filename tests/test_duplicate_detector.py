import pytest
from app.database.connection import Base, engine, SessionLocal
from app.database.models import Complaint
from app.ai.duplicate_detector import detect_duplicates


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Add seed complaints
    c1 = Complaint(complaint_id="RAI-101", complaint_text="AC is not cooling in coach B4.", complaint_type="Air Conditioning")
    c2 = Complaint(complaint_id="RAI-102", complaint_text="Food is stale and bad quality.", complaint_type="Catering")
    db.add_all([c1, c2])
    db.commit()
    yield
    db.close()


def test_duplicate_detection_high_similarity():
    db = SessionLocal()
    res = detect_duplicates("AC cooling is stopped in coach B4.", db, threshold=0.30)
    assert res["is_duplicate"] is True
    assert res["matched_complaint_id"] == "RAI-101"
    db.close()


def test_duplicate_detection_low_similarity():
    db = SessionLocal()
    res = detect_duplicates("Doctor needed immediately for chest pain.", db, threshold=0.80)
    assert res["is_duplicate"] is False
    db.close()


def test_duplicate_detection_empty_input():
    db = SessionLocal()
    res = detect_duplicates("", db)
    assert res["is_duplicate"] is False
    assert res["similarity_score"] == 0.0
    db.close()
