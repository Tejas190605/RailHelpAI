import pytest
from app.ai.resolution_predictor import resolution_predictor_service


def test_predict_resolution_time_ac():
    res = resolution_predictor_service.predict_resolution_time(
        category="Air Conditioning",
        priority="P2",
        department="Electrical / Coach Maintenance",
        train_number="12951",
        station="Pune"
    )
    assert res["predicted_resolution_minutes"] > 0
    assert "predicted_resolution_human" in res
    assert res["prediction_confidence"] == "Medium"


def test_predict_resolution_time_medical_fast():
    res = resolution_predictor_service.predict_resolution_time(
        category="Medical",
        priority="P1",
        department="Medical Emergency Response",
        train_number="12261",
        station="Mumbai"
    )
    # Medical P1 should be faster than AC P2
    assert res["predicted_resolution_minutes"] >= 10.0
