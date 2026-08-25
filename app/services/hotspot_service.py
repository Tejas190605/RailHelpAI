from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.models import Complaint, ComplaintCluster
from app.services.sla_engine import evaluate_sla_status


def get_hotspot_analytics(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Compute multi-factor hotspot risk scores for trains and stations.
    Formula:
    Hotspot Score = (Volume * 0.35) + (Severity * 0.30) + (SLA Breach Rate * 0.20) + (Cluster Activity * 0.15)
    """
    # Group complaints by Train Number
    train_counts = db.query(Complaint.train_number, func.count(Complaint.id)).filter(Complaint.train_number.isnot(None)).group_by(Complaint.train_number).all()

    hotspots = []
    max_vol = max([tc[1] for tc in train_counts], default=1)

    for train_num, vol in train_counts:
        train_complaints = db.query(Complaint).filter(Complaint.train_number == train_num).all()
        
        # 1. Volume Score (0-100)
        vol_score = min((vol / max_vol) * 100.0, 100.0)

        # 2. Severity Score (0-100)
        p1_count = sum(1 for c in train_complaints if c.priority == "P1")
        p2_count = sum(1 for c in train_complaints if c.priority == "P2")
        sev_score = min(((p1_count * 2.0 + p2_count * 1.0) / max(vol, 1)) * 50.0, 100.0)

        # 3. SLA Breach Rate (0-100)
        breached_count = sum(1 for c in train_complaints if evaluate_sla_status(c.created_at, c.sla_deadline, c.resolved_at)["is_breached"])
        breach_rate = (breached_count / vol) * 100.0

        # 4. Cluster Activity (0-100)
        cluster_count = db.query(ComplaintCluster).join(Complaint).filter(Complaint.train_number == train_num).count()
        cluster_score = min(cluster_count * 20.0, 100.0)

        total_score = round(
            (vol_score * 0.35) + (sev_score * 0.30) + (breach_rate * 0.20) + (cluster_score * 0.15),
            1
        )

        if total_score >= 80.0:
            risk = "CRITICAL"
        elif total_score >= 60.0:
            risk = "HIGH"
        elif total_score >= 30.0:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        hotspots.append({
            "target_type": "Train",
            "identifier": train_num,
            "hotspot_score": total_score,
            "risk_level": risk,
            "total_complaints": vol,
            "critical_p1_count": p1_count,
            "sla_breach_count": breached_count,
            "active_clusters": cluster_count
        })

    hotspots.sort(key=lambda x: x["hotspot_score"], reverse=True)
    return hotspots[:limit]
