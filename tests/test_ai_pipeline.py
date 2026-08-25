import pytest
from app.ai.pipeline import analyze_complaint
from app.backend.schemas.ai_schema import AIAnalysisResult


def test_unified_ai_pipeline_execution():
    text = "AC isn't cooling in coach B4 seat 21 and we've been waiting for 30 minutes since Pune on train 12951."
    res = analyze_complaint(text)

    assert isinstance(res, AIAnalysisResult)
    assert res.category.value == "Air Conditioning"
    assert res.category.confidence > 0.0
    assert res.entities.get("coach") == "B4"
    assert "21" in res.entities.get("seats", [])
    assert res.priority.level in ["P1", "P2"]
    assert res.department.name == "Electrical / Coach Maintenance"
    assert res.routing_mode in ["AUTOMATIC", "HUMAN_REVIEW", "MANUAL"]
    assert len(res.priority.reasons) > 0


def test_pipeline_empty_input_fallback():
    res = analyze_complaint("")
    assert res.category.value == "Other"
    assert res.routing_mode == "MANUAL"
    assert res.human_review_required is True
