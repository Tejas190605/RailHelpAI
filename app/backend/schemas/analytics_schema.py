from typing import Dict, Any, List, Optional
from pydantic import BaseModel, ConfigDict


class OverviewKPIsResponse(BaseModel):
    total_complaints: int
    open_complaints: int
    resolved_complaints: int
    critical_complaints: int
    sla_breaches: int
    avg_response_time_mins: float
    avg_resolution_time_mins: float
    ai_automation_rate: float
    sla_compliance_rate: float

    model_config = ConfigDict(from_attributes=True)


class CategoryBreakdownItem(BaseModel):
    category: str
    count: int


class PriorityBreakdownItem(BaseModel):
    priority: str
    count: int


class DepartmentWorkloadItem(BaseModel):
    department: str
    open_count: int


class SLAPerformanceSummary(BaseModel):
    WITHIN_SLA: int
    APPROACHING_SLA: int
    ESCALATION_WARNING: int
    BREACHED: int
