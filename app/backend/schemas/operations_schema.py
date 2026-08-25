from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class AssignComplaintRequest(BaseModel):
    department: str = Field(..., json_schema_extra={"example": "Electrical / Coach Maintenance"})
    assigned_to: Optional[str] = Field("Operator Agent", json_schema_extra={"example": "Agent #104"})


class HumanReviewRequest(BaseModel):
    reviewer: str = Field("Operator Admin", json_schema_extra={"example": "Supervisor Vijay"})
    action: str = Field("Approve", json_schema_extra={"example": "Approve"})  # Approve or Override
    final_category: Optional[str] = None
    final_priority: Optional[str] = None
    final_department: Optional[str] = None
    reason: Optional[str] = None


class ResolveComplaintRequest(BaseModel):
    resolution_text: str = Field(..., min_length=5, json_schema_extra={"example": "Replaced faulty AC capacitor in coach B4."})
    resolution_type: str = Field("FIXED", json_schema_extra={"example": "FIXED"})
    resolved_by: Optional[str] = Field("System Operator", json_schema_extra={"example": "Technician Ramesh"})


class FeedbackRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5, json_schema_extra={"example": 5})
    feedback: Optional[str] = Field(None, json_schema_extra={"example": "Quick resolution, thanks!"})


class AIReviewResponse(BaseModel):
    id: int
    complaint_id: int
    reviewer: str
    original_category: Optional[str] = None
    final_category: Optional[str] = None
    original_priority: Optional[str] = None
    final_priority: Optional[str] = None
    original_department: Optional[str] = None
    final_department: Optional[str] = None
    action: str
    reason: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
