from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional, Tuple

# Prototype SLA Policy Targets (Minutes)
# Important: Demonstration values only; not official Indian Railways commitments.
SLA_POLICY_MINUTES = {
    "P1": {"response_minutes": 10, "resolution_minutes": 30},
    "P2": {"response_minutes": 30, "resolution_minutes": 120},
    "P3": {"response_minutes": 120, "resolution_minutes": 480},
    "P4": {"response_minutes": 480, "resolution_minutes": 1440}
}


def calculate_sla_deadlines(priority: str, created_at: Optional[datetime] = None) -> Tuple[datetime, datetime]:
    """
    Calculate response deadline and resolution deadline based on priority level.
    Returns (response_deadline, resolution_deadline).
    """
    if created_at is None:
        created_at = datetime.now(timezone.utc)
    elif created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    policy = SLA_POLICY_MINUTES.get(priority, SLA_POLICY_MINUTES["P3"])

    response_deadline = created_at + timedelta(minutes=policy["response_minutes"])
    resolution_deadline = created_at + timedelta(minutes=policy["resolution_minutes"])

    return response_deadline, resolution_deadline


def evaluate_sla_status(
    created_at: datetime,
    deadline: Optional[datetime],
    resolved_at: Optional[datetime] = None,
    current_time: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    Dynamically evaluate SLA status, elapsed percentage, and remaining time in minutes.
    Statuses: WITHIN_SLA, APPROACHING_SLA, ESCALATION_WARNING, BREACHED.
    """
    if current_time is None:
        current_time = datetime.now(timezone.utc)
    elif current_time.tzinfo is None:
        current_time = current_time.replace(tzinfo=timezone.utc)

    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    if deadline is None:
        deadline = created_at + timedelta(hours=8)
    elif deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=timezone.utc)

    if resolved_at and resolved_at.tzinfo is None:
        resolved_at = resolved_at.replace(tzinfo=timezone.utc)

    # Use resolved_at if resolved, otherwise current_time
    effective_end = resolved_at if resolved_at else current_time

    total_seconds = (deadline - created_at).total_seconds()
    if total_seconds <= 0:
        total_seconds = 1.0

    elapsed_seconds = (effective_end - created_at).total_seconds()
    remaining_seconds = (deadline - effective_end).total_seconds()

    pct_elapsed = round((elapsed_seconds / total_seconds) * 100.0, 1)
    remaining_minutes = round(remaining_seconds / 60.0, 1)

    if resolved_at:
        is_breached = resolved_at > deadline
        status = "BREACHED" if is_breached else "WITHIN_SLA"
    else:
        if current_time > deadline or pct_elapsed >= 100.0:
            status = "BREACHED"
        elif pct_elapsed >= 90.0:
            status = "ESCALATION_WARNING"
        elif pct_elapsed >= 50.0:
            status = "APPROACHING_SLA"
        else:
            status = "WITHIN_SLA"

    return {
        "sla_status": status,
        "pct_elapsed": min(pct_elapsed, 100.0) if not is_breached_check(status) else max(pct_elapsed, 100.0),
        "remaining_minutes": max(remaining_minutes, 0.0) if status != "BREACHED" else remaining_minutes,
        "is_breached": status == "BREACHED"
    }


def is_breached_check(status: str) -> bool:
    return status == "BREACHED"
