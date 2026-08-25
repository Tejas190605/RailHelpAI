import pytest
from app.ai.classifier import classifier_service, ComplaintClassifier


def test_classifier_model_loading():
    assert classifier_service is not None


def test_classifier_prediction_ac():
    res = classifier_service.predict("AC is not cooling in coach B4 seat 21.")
    assert res["category"] == "Air Conditioning"
    assert "confidence" in res
    assert res["confidence"] > 0.0
    assert res["model_name"] == "complaint_classifier"


def test_classifier_prediction_cleanliness():
    res = classifier_service.predict("Toilet is extremely dirty and trash is overflowing.")
    assert res["category"] == "Cleanliness"


def test_classifier_empty_input():
    res = classifier_service.predict("")
    assert res["category"] == "Other"
    assert res["confidence"] == 0.0
