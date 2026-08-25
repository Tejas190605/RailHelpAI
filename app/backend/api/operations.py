from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Complaint, Assignment, Resolution, AIReview, AIPrediction
from app.services.workflow import validate_state_transition
from app.backend.schemas.complaint_schema import ComplaintResponse
from app.backend.schemas.operations_schema import (
    AssignComplaintRequest, HumanReviewRequest, ResolveComplaintRequest,
    FeedbackRequest, AIReviewResponse
)

router = APIRouter(prefix="/complaints", tags=["Operations & Workflow"])


def find_complaint_or_404(db: Session, complaint_ref: str) -> Complaint:
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
    return complaint


@router.post("/{complaint_ref}/assign", response_model=ComplaintResponse)
def assign_complaint(
    complaint_ref: str,
    payload: AssignComplaintRequest,
    db: Session = Depends(get_db)
):
    """Assign complaint to a department and operator."""
    complaint = find_complaint_or_404(db, complaint_ref)

    if not validate_state_transition(complaint.status, "ASSIGNED"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid state transition from '{complaint.status}' to 'ASSIGNED'."
        )

    complaint.department = payload.department
    complaint.assigned_to = payload.assigned_to or "Operator Agent"
    complaint.assigned_at = datetime.now(timezone.utc)
    complaint.status = "ASSIGNED"
    complaint.updated_at = datetime.now(timezone.utc)

    # Save assignment record
    assignment_record = Assignment(
        complaint_id=complaint.id,
        department=payload.department,
        assigned_to=payload.assigned_to,
        assigned_at=datetime.now(timezone.utc),
        status="ASSIGNED"
    )
    db.add(assignment_record)
    db.commit()
    db.refresh(complaint)
    return complaint


@router.post("/{complaint_ref}/review", response_model=ComplaintResponse)
def review_complaint_ai(
    complaint_ref: str,
    payload: HumanReviewRequest,
    db: Session = Depends(get_db)
):
    """Process human review for an AI-analyzed complaint (Approve or Override predictions)."""
    complaint = find_complaint_or_404(db, complaint_ref)

    orig_category = complaint.complaint_type
    orig_priority = complaint.priority
    orig_dept = complaint.department

    if payload.action == "Override":
        if payload.final_category:
            complaint.complaint_type = payload.final_category
        if payload.final_priority:
            complaint.priority = payload.final_priority
        if payload.final_department:
            complaint.department = payload.final_department

    complaint.status = "ASSIGNED"
    complaint.assigned_at = datetime.now(timezone.utc)
    complaint.updated_at = datetime.now(timezone.utc)

    review_audit = AIReview(
        complaint_id=complaint.id,
        reviewer=payload.reviewer,
        original_category=orig_category,
        final_category=complaint.complaint_type,
        original_priority=orig_priority,
        final_priority=complaint.priority,
        original_department=orig_dept,
        final_department=complaint.department,
        action=payload.action,
        reason=payload.reason
    )
    db.add(review_audit)
    db.commit()
    db.refresh(complaint)
    return complaint


@router.post("/{complaint_ref}/resolve", response_model=ComplaintResponse)
def resolve_complaint(
    complaint_ref: str,
    payload: ResolveComplaintRequest,
    db: Session = Depends(get_db)
):
    """Resolve a complaint with operator resolution text and type."""
    complaint = find_complaint_or_404(db, complaint_ref)

    if complaint.status == "RESOLVED" or complaint.status == "CLOSED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Complaint is already '{complaint.status}'."
        )

    now = datetime.now(timezone.utc)
    created_at = complaint.created_at
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    duration_mins = round((now - created_at).total_seconds() / 60.0, 1)

    complaint.status = "RESOLVED"
    complaint.resolved_at = now
    complaint.updated_at = now

    resolution_record = Resolution(
        complaint_id=complaint.id,
        resolution_text=payload.resolution_text,
        resolution_type=payload.resolution_type,
        resolved_at=now,
        resolution_time_minutes=duration_mins
    )
    db.add(resolution_record)
    db.commit()
    db.refresh(complaint)
    return complaint


@router.post("/{complaint_ref}/feedback", response_model=ComplaintResponse)
def submit_feedback(
    complaint_ref: str,
    payload: FeedbackRequest,
    db: Session = Depends(get_db)
):
    """Record passenger satisfaction rating (1-5) and feedback notes."""
    complaint = find_complaint_or_404(db, complaint_ref)

    complaint.rating = payload.rating
    complaint.feedback = payload.feedback
    complaint.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(complaint)
    return complaint
