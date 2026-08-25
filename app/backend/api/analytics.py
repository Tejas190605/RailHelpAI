from fastapi import APIRouter, Depends
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.analytics_service import (
    get_overview_kpis, get_category_breakdown, get_priority_breakdown,
    get_department_workload, get_sla_performance_summary
)
from app.backend.schemas.analytics_schema import (
    OverviewKPIsResponse, CategoryBreakdownItem, PriorityBreakdownItem,
    DepartmentWorkloadItem, SLAPerformanceSummary
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview", response_model=OverviewKPIsResponse)
def overview_kpis_endpoint(db: Session = Depends(get_db)):
    """Fetch database-derived operational KPIs."""
    return get_overview_kpis(db)


@router.get("/categories", response_model=List[CategoryBreakdownItem])
def category_breakdown_endpoint(db: Session = Depends(get_db)):
    """Fetch complaint count breakdown by category."""
    return get_category_breakdown(db)


@router.get("/priority", response_model=List[PriorityBreakdownItem])
def priority_breakdown_endpoint(db: Session = Depends(get_db)):
    """Fetch complaint count breakdown by priority level."""
    return get_priority_breakdown(db)


@router.get("/departments", response_model=List[DepartmentWorkloadItem])
def department_workload_endpoint(db: Session = Depends(get_db)):
    """Fetch open complaint workload per department."""
    return get_department_workload(db)


@router.get("/sla", response_model=SLAPerformanceSummary)
def sla_performance_endpoint(db: Session = Depends(get_db)):
    """Fetch SLA compliance performance distribution."""
    return get_sla_performance_summary(db)
