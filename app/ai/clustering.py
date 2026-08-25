import logging
from typing import Dict, Any, List
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN

from app.database.models import Complaint, ComplaintCluster
from app.ai.preprocessor import preprocess_text

logger = logging.getLogger(__name__)


def rebuild_incident_clusters(
    db: Session,
    eps: float = 0.65,
    min_samples: int = 2
) -> Dict[str, Any]:
    """
    Run DBSCAN clustering across open complaints to group recurring incidents.
    Persists results to complaint_clusters table.
    """
    complaints = db.query(Complaint).order_by(Complaint.id.desc()).limit(1000).all()
    if not complaints or len(complaints) < min_samples:
        return {
            "total_complaints_analyzed": len(complaints) if complaints else 0,
            "total_clusters_found": 0,
            "clusters": [],
            "status": "INSUFFICIENT_DATA"
        }

    texts = [preprocess_text(c.complaint_text) for c in complaints]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=2500, sublinear_tf=True)

    try:
        tfidf_matrix = vectorizer.fit_transform(texts)
    except Exception as e:
        logger.error(f"Clustering TF-IDF error: {e}")
        return {"total_complaints_analyzed": len(complaints), "total_clusters_found": 0, "clusters": [], "status": "ERROR"}

    # DBSCAN algorithm using cosine distance
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric="cosine")
    labels = dbscan.fit_predict(tfidf_matrix)

    # Clear existing clusters table
    db.query(ComplaintCluster).delete()

    cluster_groups: Dict[int, List[Complaint]] = {}
    for idx, label in enumerate(labels):
        if label != -1:  # -1 represents noise / unclustered complaints
            if label not in cluster_groups:
                cluster_groups[label] = []
            cluster_groups[label].append(complaints[idx])

    summary_list = []
    for cluster_num, comp_list in cluster_groups.items():
        cid = f"INC-{cluster_num + 1:03d}"
        
        # Primary category and metadata
        categories = [c.complaint_type for c in comp_list if c.complaint_type]
        top_cat = max(set(categories), key=categories.count) if categories else "General"
        coaches = [c.coach for c in comp_list if c.coach]
        top_coach = max(set(coaches), key=coaches.count) if coaches else "Train Wide"

        label_title = f"{top_cat} Incident — Coach {top_coach} ({len(comp_list)} reports)"

        for c in comp_list:
            cc = ComplaintCluster(
                cluster_id=cid,
                complaint_id=c.id,
                similarity_score=0.85,
                cluster_label=label_title
            )
            db.add(cc)

        summary_list.append({
            "cluster_id": cid,
            "cluster_label": label_title,
            "complaint_count": len(comp_list),
            "common_category": top_cat,
            "common_coach": top_coach,
            "status": "ACTIVE"
        })

    db.commit()

    return {
        "total_complaints_analyzed": len(complaints),
        "total_clusters_found": len(cluster_groups),
        "clusters": summary_list,
        "status": "SUCCESS"
    }


from sqlalchemy import func


def get_active_clusters(db: Session) -> List[Dict[str, Any]]:
    """Retrieve summarized incident clusters from database."""
    clusters = db.query(ComplaintCluster.cluster_id, ComplaintCluster.cluster_label, func.count(ComplaintCluster.id))\
                .group_by(ComplaintCluster.cluster_id, ComplaintCluster.cluster_label).all()

    return [
        {
            "cluster_id": r[0],
            "cluster_label": r[1],
            "complaint_count": r[2],
            "status": "ACTIVE"
        }
        for r in clusters
    ]
