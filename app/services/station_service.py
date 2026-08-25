from typing import Dict, Any, List
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.models import Complaint
from app.services.sla_engine import evaluate_sla_status


def get_stations_summary(db: Session) -> List[Dict[str, Any]]:
    """Get summarized analytics across all stations."""
    station_results = db.query(Complaint.station, func.count(Complaint.id)).filter(Complaint.station.isnot(None)).group_by(Complaint.station).all()

    summary = []
    for station_name, count in station_results:
        summary.append({
            "station_name": station_name,
            "total_complaints": count
        })
    return summary


def get_station_profile(db: Session, station_name: str) -> Dict[str, Any]:
    """Get deep analytical profile for a specific station."""
    complaints = db.query(Complaint).filter(Complaint.station == station_name).all()
    if not complaints:
        return {
            "station_name": station_name,
            "total_complaints": 0,
            "open_complaints": 0,
            "resolved_complaints": 0,
            "top_categories": [],
            "sla_compliance_rate": 100.0
        }

    total = len(complaints)
    open_cnt = sum(1 for c in complaints if c.status not in ["Resolved", "Closed"])
    resolved_cnt = sum(1 for c in complaints if c.status == "Resolved")

    # Category counts
    cats = [c.complaint_type for c in complaints if c.complaint_type]
    top_cats = [{"category": k, "count": v} for k, v in pd.Series(cats).value_counts().head(5).items()] if cats else []

    # SLA compliance
    resolved_within = 0
    for c in complaints:
        if c.status == "Resolved":
            if not evaluate_sla_status(c.created_at, c.sla_deadline, c.resolved_at)["is_breached"]:
                resolved_within += 1

    sla_rate = (resolved_within / resolved_cnt * 100.0) if resolved_cnt > 0 else 100.0

    return {
        "station_name": station_name,
        "total_complaints": total,
        "open_complaints": open_cnt,
        "resolved_complaints": resolved_cnt,
        "top_categories": top_cats,
        "sla_compliance_rate": round(sla_rate, 1)
    }
