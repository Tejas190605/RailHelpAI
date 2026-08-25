from typing import Dict, Any
from sqlalchemy.orm import Session

from app.database.models import Complaint, ComplaintCluster
from app.services.sla_engine import evaluate_sla_status


def calculate_operational_risk_index(db: Session) -> Dict[str, Any]:
    """
    Compute composite RailHelpAI Operational Risk Index.
    Prototype analytical score; not an official Indian Railways risk metric.
    Formula:
    Risk Index = (Volume * 0.25) + (P1 Severity * 0.30) + (SLA Breach Rate * 0.25) + (Incident Activity * 0.20)
    """
    complaints = db.query(Complaint).all()
    total = len(complaints)
    if total == 0:
        return {
            "risk_index": 0.0,
            "risk_level": "LOW",
            "components": {"volume": 0.0, "severity": 0.0, "sla_breaches": 0.0, "incidents": 0.0},
            "disclaimer": "Prototype analytical score — not an official railway risk metric."
        }

    # 1. Volume Signal
    vol_signal = min((total / 100.0) * 100.0, 100.0)

    # 2. P1 Severity Signal
    p1_count = sum(1 for c in complaints if c.priority == "P1")
    sev_signal = min((p1_count / max(total, 1)) * 200.0, 100.0)

    # 3. SLA Breach Rate Signal
    breaches = sum(1 for c in complaints if evaluate_sla_status(c.created_at, c.sla_deadline, c.resolved_at)["is_breached"])
    sla_signal = min((breaches / total) * 100.0, 100.0)

    # 4. Incident Activity Signal
    clusters = db.query(ComplaintCluster).count()
    inc_signal = min(clusters * 20.0, 100.0)

    composite_score = round(
        (vol_signal * 0.25) + (sev_signal * 0.30) + (sla_signal * 0.25) + (inc_signal * 0.20),
        1
    )

    if composite_score >= 80.0:
        level = "CRITICAL"
    elif composite_score >= 60.0:
        level = "HIGH"
    elif composite_score >= 30.0:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "risk_index": composite_score,
        "risk_level": level,
        "components": {
            "volume_score": round(vol_signal, 1),
            "severity_score": round(sev_signal, 1),
            "sla_breach_score": round(sla_signal, 1),
            "incident_cluster_score": round(inc_signal, 1)
        },
        "disclaimer": "Prototype analytical score — not an official railway risk metric."
    }
