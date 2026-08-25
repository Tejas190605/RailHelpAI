from typing import Dict, Any, List
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.models import Complaint
from app.services.sla_engine import evaluate_sla_status


def get_trains_summary(db: Session) -> List[Dict[str, Any]]:
    """Get summarized analytics across all trains."""
    train_results = db.query(Complaint.train_number, func.count(Complaint.id)).filter(Complaint.train_number.isnot(None)).group_by(Complaint.train_number).all()

    summary = []
    for train_num, count in train_results:
        summary.append({
            "train_number": train_num,
            "total_complaints": count
        })
    return summary


def get_train_profile(db: Session, train_number: str) -> Dict[str, Any]:
    """Get deep analytical profile for a specific train."""
    complaints = db.query(Complaint).filter(Complaint.train_number == train_number).all()
    if not complaints:
        return {
            "train_number": train_number,
            "total_complaints": 0,
            "open_complaints": 0,
            "resolved_complaints": 0,
            "top_categories": [],
            "worst_coaches": [],
            "sla_compliance_rate": 100.0
        }

    total = len(complaints)
    open_cnt = sum(1 for c in complaints if c.status not in ["Resolved", "Closed"])
    resolved_cnt = sum(1 for c in complaints if c.status == "Resolved")

    # Category counts
    cats = [c.complaint_type for c in complaints if c.complaint_type]
    top_cats = [{"category": k, "count": v} for k, v in pd.Series(cats).value_counts().head(5).items()] if cats else []

    # Worst coaches
    coaches = [c.coach for c in complaints if c.coach]
    worst_coaches = [{"coach": k, "count": v} for k, v in pd.Series(coaches).value_counts().head(5).items()] if coaches else []

    # SLA compliance
    resolved_within = 0
    for c in complaints:
        if c.status == "Resolved":
            if not evaluate_sla_status(c.created_at, c.sla_deadline, c.resolved_at)["is_breached"]:
                resolved_within += 1

    sla_rate = (resolved_within / resolved_cnt * 100.0) if resolved_cnt > 0 else 100.0

    return {
        "train_number": train_number,
        "total_complaints": total,
        "open_complaints": open_cnt,
        "resolved_complaints": resolved_cnt,
        "top_categories": top_cats,
        "worst_coaches": worst_coaches,
        "sla_compliance_rate": round(sla_rate, 1)
    }
