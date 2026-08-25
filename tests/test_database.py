import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base, Complaint, Department, AIReview
from app.database.connection import get_db


@pytest.fixture
def db_session():
    """Create isolated in-memory SQLite database session for testing."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    # Seed default department
    dept = Department(department_name="Electrical", category="Air Conditioning", default_sla_hours=8)
    session.add(dept)
    session.commit()
    
    try:
        yield session
    finally:
        session.close()


def test_db_schema_initialization(db_session):
    """Verify schema initialization and initial table setup."""
    departments = db_session.query(Department).all()
    assert len(departments) == 1
    assert departments[0].department_name == "Electrical"


def test_complaint_crud_lifecycle(db_session):
    """Test full CRUD lifecycle of Complaint model."""
    # Create
    complaint = Complaint(
        complaint_id="RAI-TEST001",
        complaint_text="AC not working in coach B2",
        complaint_type="Air Conditioning",
        priority="P2",
        department="Electrical",
        status="NEW"
    )
    db_session.add(complaint)
    db_session.commit()
    db_session.refresh(complaint)
    
    assert complaint.id is not None
    assert complaint.status == "NEW"
    
    # Read
    retrieved = db_session.query(Complaint).filter(Complaint.id == complaint.id).first()
    assert retrieved is not None
    assert retrieved.complaint_type == "Air Conditioning"
    
    # Update
    retrieved.status = "ASSIGNED"
    retrieved.department = "Electrical"
    db_session.commit()
    
    updated = db_session.query(Complaint).filter(Complaint.id == complaint.id).first()
    assert updated.status == "ASSIGNED"
    
    # Delete
    db_session.delete(updated)
    db_session.commit()
    
    deleted = db_session.query(Complaint).filter(Complaint.id == complaint.id).first()
    assert deleted is None


def test_transaction_rollback_on_error(db_session):
    """Verify transaction rollback preserves database integrity."""
    complaint = Complaint(
        complaint_id="RAI-TEST002",
        complaint_text="Valid complaint",
        complaint_type="Cleanliness",
        priority="P3",
        department="Medical",
        status="NEW"
    )
    db_session.add(complaint)
    db_session.commit()
    
    # Attempt invalid operation within a transaction
    try:
        invalid_review = AIReview(complaint_id=99999)  # Non-existent complaint ID
        db_session.add(invalid_review)
        db_session.flush()
    except Exception:
        db_session.rollback()
        
    # Verify original record is still intact and accessible
    existing = db_session.query(Complaint).filter(Complaint.id == complaint.id).first()
    assert existing is not None
    assert existing.complaint_text == "Valid complaint"
