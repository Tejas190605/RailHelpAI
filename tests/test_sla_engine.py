import pytest
from datetime import datetime, timedelta, timezone
from app.services.sla_engine import calculate_sla_deadlines, evaluate_sla_status


def test_calculate_sla_deadlines_p1():
    created_now = datetime.now(timezone.utc)
    resp_dl, res_dl = calculate_sla_deadlines("P1", created_now)
    assert (resp_dl - created_now).total_seconds() == 600.0  # 10 mins
    assert (res_dl - created_now).total_seconds() == 1800.0  # 30 mins


def test_calculate_sla_deadlines_p2():
    created_now = datetime.now(timezone.utc)
    resp_dl, res_dl = calculate_sla_deadlines("P2", created_now)
    assert (resp_dl - created_now).total_seconds() == 1800.0  # 30 mins
    assert (res_dl - created_now).total_seconds() == 7200.0   # 2 hours


def test_evaluate_sla_status_within():
    created_now = datetime.now(timezone.utc)
    deadline = created_now + timedelta(hours=2)
    # At created time -> Within SLA
    res = evaluate_sla_status(created_now, deadline, current_time=created_now)
    assert res["sla_status"] == "WITHIN_SLA"
    assert res["pct_elapsed"] == 0.0
    assert res["is_breached"] is False


def test_evaluate_sla_status_approaching_50pct():
    created_now = datetime.now(timezone.utc)
    deadline = created_now + timedelta(hours=2)
    current_time = created_now + timedelta(hours=1)  # 50% elapsed
    res = evaluate_sla_status(created_now, deadline, current_time=current_time)
    assert res["sla_status"] == "APPROACHING_SLA"
    assert res["pct_elapsed"] == 50.0


def test_evaluate_sla_status_escalation_warning_90pct():
    created_now = datetime.now(timezone.utc)
    deadline = created_now + timedelta(hours=2)
    current_time = created_now + timedelta(minutes=110)  # 91.6% elapsed
    res = evaluate_sla_status(created_now, deadline, current_time=current_time)
    assert res["sla_status"] == "ESCALATION_WARNING"


def test_evaluate_sla_status_breached():
    created_now = datetime.now(timezone.utc)
    deadline = created_now + timedelta(hours=2)
    current_time = created_now + timedelta(hours=3)  # Past deadline
    res = evaluate_sla_status(created_now, deadline, current_time=current_time)
    assert res["sla_status"] == "BREACHED"
    assert res["is_breached"] is True
