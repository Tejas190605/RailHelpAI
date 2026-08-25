import logging
from typing import Dict, Any, List
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.models import Complaint, ComplaintCluster
from app.services.trend_service import calculate_category_trends
from app.services.sla_engine import evaluate_sla_status

logger = logging.getLogger(__name__)


def generate_operational_recommendations(db: Session) -> List[Dict[str, Any]]:
    """
    Generate metric-backed, explainable prescriptive recommendations based on database evidence.
    No paid LLM requirement.
    """
    recommendations = []

    # Rule 1: High SLA Breach Rate in Specific Category
    complaints = db.query(Complaint).all()
    if not complaints:
        return []

    breaches_by_cat: Dict[str, int] = {}
    total_by_cat: Dict[str, int] = {}

    for c in complaints:
        cat = c.complaint_type or "Other"
        total_by_cat[cat] = total_by_cat.get(cat, 0) + 1
        if evaluate_sla_status(c.created_at, c.sla_deadline, c.resolved_at)["is_breached"]:
            breaches_by_cat[cat] = breaches_by_cat.get(cat, 0) + 1

    for cat, total in total_by_cat.items():
        breaches = breaches_by_cat.get(cat, 0)
        breach_rate = (breaches / total * 100.0) if total > 0 else 0.0

        if breach_rate >= 25.0 and total >= 3:
            recommendations.append({
                "title": f"Deploy Extra Resources for {cat}",
                "recommendation_text": f"Prioritize immediate staffing and contractor deployment for {cat} grievances due to high SLA breach frequency.",
                "severity": "HIGH",
                "supporting_metrics": f"{breaches} SLA breaches out of {total} total complaints ({round(breach_rate, 1)}% breach rate).",
                "reasoning": f"Category '{cat}' exhibits a {round(breach_rate, 1)}% SLA breach rate exceeding the 25% operational threshold.",
                "confidence": 0.90
            })

    # Rule 2: Active Incident Clusters
    active_clusters = db.query(ComplaintCluster.cluster_id, ComplaintCluster.cluster_label, func.count(ComplaintCluster.id))\
                        .group_by(ComplaintCluster.cluster_id, ComplaintCluster.cluster_label).all()

    for cid, label, cnt in active_clusters:
        if cnt >= 3:
            recommendations.append({
                "title": f"Inspect Recurring Incident {cid}",
                "recommendation_text": f"Dispatch maintenance inspection crew to address recurring incident '{label}'.",
                "severity": "CRITICAL" if cnt >= 5 else "MEDIUM",
                "supporting_metrics": f"{cnt} correlated complaints grouped under incident {cid}.",
                "reasoning": f"DBSCAN clustering identified an active incident cluster '{label}' with {cnt} recurring grievances.",
                "confidence": 0.88
            })

    # Rule 3: Category Trend Acceleration
    trends = calculate_category_trends(db)
    for t in trends:
        if t["trend"] == "INCREASING" and t["recent_7d_count"] >= 5:
            recommendations.append({
                "title": f"Monitor Surge in {t['category']} Grievances",
                "recommendation_text": f"Increase depot inspection frequency for {t['category']} complaints.",
                "severity": "MEDIUM",
                "supporting_metrics": f"{t['recent_7d_count']} recent complaints vs {t['prev_7d_count']} previous period (+{t['change_percent']}% change).",
                "reasoning": f"Category '{t['category']}' exhibits an accelerating trend (+{t['change_percent']}% 7-day surge).",
                "confidence": 0.85
            })

    return recommendations[:5]
