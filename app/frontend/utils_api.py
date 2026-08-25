import os
import requests
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000/api/v1")


def get_health() -> Dict[str, Any]:
    """Check backend service health."""
    try:
        response = requests.get(f"{BACKEND_API_URL}/health", timeout=3)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.warning(f"Health check failed: {e}")
    return {"status": "offline", "app_name": "RailHelpAI"}


def create_complaint(payload: Dict[str, Any]) -> Dict[str, Any]:
    """POST a new complaint to backend."""
    try:
        response = requests.post(f"{BACKEND_API_URL}/complaints", json=payload, timeout=5)
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except Exception as e:
        logger.error(f"Error submitting complaint: {e}")
        return {"success": False, "error": str(e)}


def get_complaints(params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Fetch complaints list with pagination & filters."""
    try:
        response = requests.get(f"{BACKEND_API_URL}/complaints", params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching complaints: {e}")
        return {"total": 0, "page": 1, "size": 20, "items": []}


def get_complaint_detail(complaint_ref: str) -> Optional[Dict[str, Any]]:
    """Fetch complaint details by ID."""
    try:
        response = requests.get(f"{BACKEND_API_URL}/complaints/{complaint_ref}", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching complaint details: {e}")
    return None


def analyze_text(text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Call stateless /ai/analyze endpoint."""
    payload = {"text": text}
    if metadata:
        payload.update(metadata)
    try:
        response = requests.post(f"{BACKEND_API_URL}/ai/analyze", json=payload, timeout=5)
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except Exception as e:
        logger.error(f"Error analyzing text: {e}")
        return {"success": False, "error": str(e)}


def assign_complaint(complaint_ref: str, department: str, assigned_to: str = "Operator Agent") -> Dict[str, Any]:
    """POST /complaints/{id}/assign."""
    try:
        response = requests.post(
            f"{BACKEND_API_URL}/complaints/{complaint_ref}/assign",
            json={"department": department, "assigned_to": assigned_to},
            timeout=5
        )
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}


def review_complaint(complaint_ref: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """POST /complaints/{id}/review."""
    try:
        response = requests.post(f"{BACKEND_API_URL}/complaints/{complaint_ref}/review", json=payload, timeout=5)
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}


def resolve_complaint(complaint_ref: str, resolution_text: str, resolution_type: str = "FIXED") -> Dict[str, Any]:
    """POST /complaints/{id}/resolve."""
    try:
        response = requests.post(
            f"{BACKEND_API_URL}/complaints/{complaint_ref}/resolve",
            json={"resolution_text": resolution_text, "resolution_type": resolution_type},
            timeout=5
        )
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}


def update_status(complaint_ref: str, status: str) -> Dict[str, Any]:
    """PATCH /complaints/{id}/status."""
    try:
        response = requests.patch(
            f"{BACKEND_API_URL}/complaints/{complaint_ref}/status",
            json={"status": status},
            timeout=5
        )
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_analytics_overview() -> Dict[str, Any]:
    """GET /analytics/overview."""
    try:
        response = requests.get(f"{BACKEND_API_URL}/analytics/overview", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching analytics overview: {e}")
    return {
        "total_complaints": 0, "open_complaints": 0, "resolved_complaints": 0,
        "critical_complaints": 0, "sla_breaches": 0, "avg_response_time_mins": 0.0,
        "avg_resolution_time_mins": 0.0, "ai_automation_rate": 100.0, "sla_compliance_rate": 100.0
    }


def detect_duplicates(text: str, threshold: float = 0.80) -> Dict[str, Any]:
    """POST /ai/detect-duplicates."""
    try:
        response = requests.post(
            f"{BACKEND_API_URL}/ai/detect-duplicates",
            json={"text": text, "threshold": threshold},
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"is_duplicate": False, "similarity_score": 0.0, "reason": str(e), "matched_complaints": []}


def predict_resolution(category: str, priority: str, department: str, train_number: str = "12951", station: str = "Pune") -> Dict[str, Any]:
    """POST /ai/predict-resolution."""
    try:
        response = requests.post(
            f"{BACKEND_API_URL}/ai/predict-resolution",
            json={"category": category, "priority": priority, "department": department, "train_number": train_number, "station": station},
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"predicted_resolution_minutes": 60.0, "predicted_resolution_human": "1h 0m", "prediction_confidence": "Medium"}


def get_clusters() -> List[Dict[str, Any]]:
    """GET /analytics/clusters."""
    try:
        res = requests.get(f"{BACKEND_API_URL}/analytics/clusters", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return []


def rebuild_clusters() -> Dict[str, Any]:
    """POST /analytics/clusters/rebuild."""
    try:
        res = requests.post(f"{BACKEND_API_URL}/analytics/clusters/rebuild", timeout=5)
        return res.json()
    except Exception as e:
        return {"status": "ERROR", "reason": str(e)}


def get_hotspots() -> List[Dict[str, Any]]:
    """GET /analytics/hotspots."""
    try:
        res = requests.get(f"{BACKEND_API_URL}/analytics/hotspots", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return []


def get_train_profile_data(train_number: str) -> Dict[str, Any]:
    """GET /analytics/trains/{train_number}."""
    try:
        res = requests.get(f"{BACKEND_API_URL}/analytics/trains/{train_number}", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return {"train_number": train_number, "total_complaints": 0, "open_complaints": 0, "resolved_complaints": 0, "top_categories": [], "worst_coaches": [], "sla_compliance_rate": 100.0}


def get_station_profile_data(station_name: str) -> Dict[str, Any]:
    """GET /analytics/stations/{station_name}."""
    try:
        res = requests.get(f"{BACKEND_API_URL}/analytics/stations/{station_name}", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return {"station_name": station_name, "total_complaints": 0, "open_complaints": 0, "resolved_complaints": 0, "top_categories": [], "sla_compliance_rate": 100.0}


def get_trends_data() -> Dict[str, Any]:
    """GET /analytics/trends."""
    try:
        res = requests.get(f"{BACKEND_API_URL}/analytics/trends", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return {"category_trends": [], "temporal_anomalies": []}


def get_recommendations_data() -> List[Dict[str, Any]]:
    """GET /analytics/recommendations."""
    try:
        res = requests.get(f"{BACKEND_API_URL}/analytics/recommendations", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return []


def get_risk_index_data() -> Dict[str, Any]:
    """GET /analytics/risk."""
    try:
        res = requests.get(f"{BACKEND_API_URL}/analytics/risk", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return {"risk_index": 0.0, "risk_level": "LOW", "components": {}, "disclaimer": "Prototype analytical score"}




