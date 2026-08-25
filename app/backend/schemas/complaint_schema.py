from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class ComplaintBase(BaseModel):
    complaint_text: str = Field(..., min_length=5, description="Full natural language description of the grievance")
    train_number: Optional[str] = Field(None, json_schema_extra={"example": "12951"})
    train_name: Optional[str] = Field(None, json_schema_extra={"example": "Rajdhani Express"})
    station: Optional[str] = Field(None, json_schema_extra={"example": "Mumbai Central"})
    coach: Optional[str] = Field(None, json_schema_extra={"example": "B4"})
    seat: Optional[str] = Field(None, json_schema_extra={"example": "21"})
    incident_datetime: Optional[datetime] = None


class ComplaintCreate(ComplaintBase):
    complaint_type: Optional[str] = "Other"
    subcategory: Optional[str] = None
    priority: Optional[str] = "P3"
    department: Optional[str] = "Unassigned"


class ComplaintUpdate(BaseModel):
    complaint_type: Optional[str] = None
    subcategory: Optional[str] = None
    priority: Optional[str] = None
    priority_score: Optional[float] = None
    sentiment: Optional[str] = None
    department: Optional[str] = None
    status: Optional[str] = None
    sla_deadline: Optional[datetime] = None


class ComplaintStatusUpdate(BaseModel):
    status: str = Field(..., json_schema_extra={"example": "In Progress"})
    notes: Optional[str] = None


class ComplaintResponse(ComplaintBase):
    id: int
    complaint_id: str
    complaint_type: str
    subcategory: Optional[str] = None
    priority: str
    priority_score: float
    sentiment: str
    language: str
    department: str
    status: str
    response_deadline: Optional[datetime] = None
    sla_deadline: Optional[datetime] = None
    assigned_to: Optional[str] = None
    assigned_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    rating: Optional[int] = None
    feedback: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ComplaintListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: List[ComplaintResponse]
