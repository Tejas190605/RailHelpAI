import pytest
from app.ai.preprocessor import preprocess_text


def test_preprocess_normal_text():
    raw = "  AC is not cooling   in coach B4 seat 21.  "
    processed = preprocess_text(raw)
    assert processed == "AC is not cooling in coach B4 seat 21."


def test_preprocess_empty_text():
    assert preprocess_text("") == ""
    assert preprocess_text(None) == ""


def test_preprocess_hinglish_normalization():
    raw = "Toilet me paani nahi aa raha aur garmi bohot hai"
    processed = preprocess_text(raw)
    assert "water" in processed.lower()
    assert "heat" in processed.lower()


def test_preprocess_preserves_tokens():
    raw = "Train 12951 coach B4 seat 42"
    processed = preprocess_text(raw)
    assert "12951" in processed
    assert "B4" in processed
    assert "42" in processed
