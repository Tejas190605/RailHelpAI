import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.models import Complaint

logger = logging.getLogger(__name__)


def calculate_category_trends(db: Session) -> List[Dict[str, Any]]:
    """
    Calculate directional volume trends across complaint categories.
    Determines INCREASING, STABLE, or DECREASING trends using real DB history.
    """
    complaints = db.query(Complaint).order_by(Complaint.created_at.desc()).all()
    if not complaints:
        return []

    df = pd.DataFrame([{
        "category": c.complaint_type or "Other",
        "created_at": c.created_at
    } for c in complaints])

    df["created_at"] = pd.to_datetime(df["created_at"])
    now = pd.Timestamp.now()

    recent_mask = df["created_at"] >= (now - pd.Timedelta(days=7))
    prev_mask = (df["created_at"] >= (now - pd.Timedelta(days=14))) & (df["created_at"] < (now - pd.Timedelta(days=7)))

    recent_counts = df[recent_mask]["category"].value_counts().to_dict()
    prev_counts = df[prev_mask]["category"].value_counts().to_dict()

    all_cats = set(recent_counts.keys()).union(set(prev_counts.keys()))
    trend_results = []

    for cat in all_cats:
        rec_cnt = recent_counts.get(cat, 0)
        prev_cnt = prev_counts.get(cat, 0)

        if prev_cnt > 0:
            pct_change = round(((rec_cnt - prev_cnt) / prev_cnt) * 100.0, 1)
        else:
            pct_change = 100.0 if rec_cnt > 0 else 0.0

        if pct_change >= 20.0:
            trend_str = "INCREASING"
        elif pct_change <= -20.0:
            trend_str = "DECREASING"
        else:
            trend_str = "STABLE"

        trend_results.append({
            "category": cat,
            "recent_7d_count": rec_cnt,
            "prev_7d_count": prev_cnt,
            "change_percent": pct_change,
            "trend": trend_str
        })

    trend_results.sort(key=lambda x: x["recent_7d_count"], reverse=True)
    return trend_results


def detect_temporal_anomalies(db: Session) -> List[Dict[str, Any]]:
    """
    Detect statistical volume spikes using rolling mean + 2 std baseline.
    """
    complaints = db.query(Complaint).order_by(Complaint.created_at.asc()).all()
    if len(complaints) < 5:
        return []

    df = pd.DataFrame([{"created_at": c.created_at, "id": c.id} for c in complaints])
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["hour"] = df["created_at"].dt.floor("h")

    hourly_counts = df.groupby("hour").size().reset_index(name="count")
    if len(hourly_counts) < 3:
        return []

    mean = hourly_counts["count"].mean()
    std = hourly_counts["count"].std()
    threshold = mean + (2.0 * std) if not np.isnan(std) and std > 0 else mean + 2.0

    anomalies = hourly_counts[hourly_counts["count"] > threshold]

    results = []
    for _, row in anomalies.iterrows():
        results.append({
            "timestamp": row["hour"].isoformat(),
            "count": int(row["count"]),
            "baseline_mean": round(float(mean), 1),
            "threshold": round(float(threshold), 1),
            "severity": "HIGH" if row["count"] > (threshold * 1.5) else "MEDIUM"
        })
    return results
