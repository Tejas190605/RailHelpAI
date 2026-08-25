from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class DuplicateDetectRequest(BaseModel):
    text: str = Field(..., min_length=5, json_schema_extra={"example": "AC not working in coach B4."})
    threshold: Optional[float] = Field(0.80, ge=0.0, le=1.0)


class MatchedComplaintItem(BaseModel):
    id: int
    complaint_id: str
    complaint_text: str
    category: Optional[str] = None
    similarity_score: float


class DuplicateDetectResponse(BaseModel):
    is_duplicate: bool
    similarity_score: float
    matched_complaint_id: Optional[str] = None
    matched_complaints: List[MatchedComplaintItem]
    threshold: float
    model_name: str
    model_version: str
    reason: str


class ResolutionPredictRequest(BaseModel):
    category: str = Field(..., json_schema_extra={"example": "Air Conditioning"})
    priority: str = Field("P2", json_schema_extra={"example": "P2"})
    department: str = Field("Electrical / Coach Maintenance", json_schema_extra={"example": "Electrical / Coach Maintenance"})
    train_number: Optional[str] = Field("12951", json_schema_extra={"example": "12951"})
    station: Optional[str] = Field("Pune", json_schema_extra={"example": "Pune"})


class ResolutionPredictResponse(BaseModel):
    predicted_resolution_minutes: float
    predicted_resolution_human: str
    prediction_confidence: str
    model_name: str
    model_version: str


class ClusterItemResponse(BaseModel):
    cluster_id: str
    cluster_label: str
    complaint_count: int
    status: str


class HotspotItemResponse(BaseModel):
    target_type: str
    identifier: str
    hotspot_score: float
    risk_level: str
    total_complaints: int
    critical_p1_count: int
    sla_breach_count: int
    active_clusters: int
