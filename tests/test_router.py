import pytest
from app.ai.router import route_department


def test_router_ac_to_electrical():
    res = route_department("Air Conditioning")
    assert res["department"] == "Electrical / Coach Maintenance"
    assert res["routing_confidence"] >= 0.85


def test_router_cleanliness_to_housekeeping():
    res = route_department("Cleanliness")
    assert res["department"] == "Housekeeping / Sanitation"


def test_router_rpf_keyword_override():
    res = route_department("Other", text="Theft reported in coach B2, please call RPF police.")
    assert res["department"] == "Railway Protection Force (RPF)"
    assert "RPF" in res["routing_reason"]
