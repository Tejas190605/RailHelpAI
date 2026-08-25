import pytest
from app.ai.priority_engine import calculate_priority


def test_priority_p1_critical_medical():
    text = "Medical emergency in coach A1 seat 14. Passenger experiencing severe chest pain."
    res = calculate_priority("Medical", text, {"coach": "A1", "seat": "14"}, "Critical")
    assert res["priority_level"] == "P1"
    assert res["priority_score"] >= 80.0
    assert len(res["reasons"]) > 0


def test_priority_p2_high_ac():
    text = "AC not cooling in coach B4 seat 21 and we have been waiting for 45 minutes since Pune."
    entities = {"coach": "B4", "seat": "21", "station": "Pune", "duration": "45 minutes"}
    res = calculate_priority("Air Conditioning", text, entities, "Angry")
    assert res["priority_level"] in ["P1", "P2"]
    assert res["priority_score"] >= 55.0


def test_priority_p3_medium_cleanliness():
    text = "Dustbin overflowing near gate in coach S3."
    res = calculate_priority("Cleanliness", text, {"coach": "S3"}, "Negative")
    assert res["priority_level"] in ["P3", "P4"]


def test_sentiment_not_sole_determinant():
    # Even if passenger is Angry, a general minor inquiry should not jump straight to P1
    text = "This is ridiculous! Why is train delayed by 5 minutes?"
    res = calculate_priority("Other", text, {}, "Angry")
    assert res["priority_level"] not in ["P1"]
