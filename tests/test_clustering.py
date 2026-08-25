import pytest
from app.database.connection import Base, engine, SessionLocal
from app.database.models import Complaint
from app.ai.clustering import rebuild_incident_clusters, get_active_clusters


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Add seed complaints for clustering
    c1 = Complaint(complaint_id="RAI-C01", complaint_text="AC is not cooling in coach B4 seat 12.", complaint_type="Air Conditioning", coach="B4")
    c2 = Complaint(complaint_id="RAI-C02", complaint_text="AC failure in coach B4 seat 25.", complaint_type="Air Conditioning", coach="B4")
    db.add_all([c1, c2])
    db.commit()
    yield
    db.close()


def test_rebuild_incident_clusters():
    db = SessionLocal()
    res = rebuild_incident_clusters(db, eps=0.80, min_samples=2)
    assert res["status"] == "SUCCESS"
    assert res["total_clusters_found"] >= 1
    db.close()


def test_get_active_clusters():
    db = SessionLocal()
    rebuild_incident_clusters(db, eps=0.80, min_samples=2)
    clusters = get_active_clusters(db)
    assert len(clusters) >= 1
    assert "cluster_id" in clusters[0]
    db.close()
