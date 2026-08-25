import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database.connection import get_db
from app.database.models import Complaint, AIPrediction
from app.ai.pipeline import analyze_complaint
from app.services.sla_engine import calculate_sla_deadlines
from app.backend.schemas.complaint_schema import (
    ComplaintCreate, ComplaintResponse, ComplaintUpdate,
    ComplaintStatusUpdate, ComplaintListResponse
)

router = APIRouter(prefix="/complaints", tags=["Complaints"])


def generate_complaint_id() -> str:
    """Generate a unique complaint ID string e.g. RAI-8F3A2B1C."""
    short_hash = uuid.uuid4().hex[:8].upper()
    return f"RAI-{short_hash}"


@router.post("", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
def create_complaint(
    payload: ComplaintCreate,
    db: Session = Depends(get_db)
):
    """Create a new complaint record with automated AI intelligence & SLA deadline calculation."""
    # Run AI Analysis Pipeline
    metadata = {
        "train_number": payload.train_number,
        "station": payload.station,
        "coach": payload.coach,
        "seat": payload.seat
    }
    ai_res = analyze_complaint(payload.complaint_text, metadata)

    created_now = datetime.now(timezone.utc)
    resp_deadline, res_deadline = calculate_sla_deadlines(ai_res.priority.level, created_now)

    # Initial status based on HITL confidence policy
    initial_status = "ASSIGNED" if ai_res.routing_mode == "AUTOMATIC" else "PENDING_REVIEW"

    complaint = Complaint(
        complaint_id=generate_complaint_id(),
        complaint_text=payload.complaint_text,
        complaint_type=ai_res.category.value,
        subcategory=ai_res.category.subcategory,
        train_number=payload.train_number or ai_res.entities.get("train_number"),
        train_name=payload.train_name,
        station=payload.station or ai_res.entities.get("station"),
        coach=payload.coach or ai_res.entities.get("coach"),
        seat=payload.seat or ai_res.entities.get("seat"),
        incident_datetime=payload.incident_datetime or created_now,
        priority=ai_res.priority.level,
        priority_score=ai_res.priority.score,
        sentiment=ai_res.sentiment.label,
        language="en",
        department=ai_res.department.name,
        status=initial_status,
        response_deadline=resp_deadline,
        sla_deadline=res_deadline,
        assigned_to="System Auto-Router" if initial_status == "ASSIGNED" else None,
        assigned_at=created_now if initial_status == "ASSIGNED" else None,
        created_at=created_now
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)

    # Store AI prediction audit log
    prediction_record = AIPrediction(
        complaint_id=complaint.id,
        model_name=ai_res.category.model_name,
        model_version=ai_res.category.model_version,
        category=ai_res.category.value,
        category_confidence=ai_res.category.confidence,
        priority=ai_res.priority.level,
        priority_confidence=ai_res.priority.confidence,
        sentiment=ai_res.sentiment.label,
        sentiment_confidence=ai_res.sentiment.confidence
    )
    db.add(prediction_record)
    db.commit()

    return complaint


@router.get("", response_model=ComplaintListResponse)
def list_complaints(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority (P1, P2, P3, P4)"),
    category: Optional[str] = Query(None, description="Filter by complaint category"),
    train_number: Optional[str] = Query(None, description="Filter by train number"),
    station: Optional[str] = Query(None, description="Filter by station name"),
    search: Optional[str] = Query(None, description="Free text search in complaint description"),
    db: Session = Depends(get_db)
):
    """Retrieve complaints list with pagination and filtering."""
    query = db.query(Complaint)

    if status:
        query = query.filter(Complaint.status == status)
    if priority:
        query = query.filter(Complaint.priority == priority)
    if category:
        query = query.filter(Complaint.complaint_type == category)
    if train_number:
        query = query.filter(Complaint.train_number == train_number)
    if station:
        query = query.filter(Complaint.station.ilike(f"%{station}%"))
    if search:
        query = query.filter(
            or_(
                Complaint.complaint_text.ilike(f"%{search}%"),
                Complaint.complaint_id.ilike(f"%{search}%")
            )
        )

    total = query.count()
    offset = (page - 1) * size
    items = query.order_by(Complaint.created_at.desc()).offset(offset).limit(size).all()

    return ComplaintListResponse(
        total=total,
        page=page,
        size=size,
        items=items
    )


@router.get("/{complaint_ref}", response_model=ComplaintResponse)
def get_complaint(
    complaint_ref: str,
    db: Session = Depends(get_db)
):
    """Fetch complaint details by integer ID or string complaint_id."""
    complaint = None
    if complaint_ref.isdigit():
        complaint = db.query(Complaint).filter(Complaint.id == int(complaint_ref)).first()
    
    if not complaint:
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_ref).first()

    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint with reference '{complaint_ref}' not found."
        )

    return complaint


@router.patch("/{complaint_ref}", response_model=ComplaintResponse)
def update_complaint(
    complaint_ref: str,
    payload: ComplaintUpdate,
    db: Session = Depends(get_db)
):
    """Update complaint fields."""
    complaint = None
    if complaint_ref.isdigit():
        complaint = db.query(Complaint).filter(Complaint.id == int(complaint_ref)).first()
    if not complaint:
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_ref).first()

    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint '{complaint_ref}' not found."
        )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(complaint, field, value)

    complaint.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(complaint)
    return complaint


@router.patch("/{complaint_ref}/status", response_model=ComplaintResponse)
def update_complaint_status(
    complaint_ref: str,
    payload: ComplaintStatusUpdate,
    db: Session = Depends(get_db)
):
    """Update the operational status of a complaint."""
    complaint = None
    if complaint_ref.isdigit():
        complaint = db.query(Complaint).filter(Complaint.id == int(complaint_ref)).first()
    if not complaint:
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_ref).first()

    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint '{complaint_ref}' not found."
        )

    complaint.status = payload.status
    if payload.status == "Resolved" and not complaint.resolved_at:
        complaint.resolved_at = datetime.now(timezone.utc)

    complaint.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(complaint)
    return complaint


@router.delete("/{complaint_ref}", status_code=status.HTTP_204_NO_CONTENT)
def delete_complaint(
    complaint_ref: str,
    db: Session = Depends(get_db)
):
    """Delete a complaint record."""
    complaint = None
    if complaint_ref.isdigit():
        complaint = db.query(Complaint).filter(Complaint.id == int(complaint_ref)).first()
    if not complaint:
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_ref).first()

    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint '{complaint_ref}' not found."
        )

    db.delete(complaint)
    db.commit()
    return None
