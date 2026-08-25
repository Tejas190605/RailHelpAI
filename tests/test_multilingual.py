import pytest
from app.ai.multilingual import detect_language, normalize_multilingual_text


def test_detect_language_english():
    res = detect_language("AC is not working in coach B4.")
    assert res["language"] == "English"
    assert res["is_multilingual"] is False


def test_detect_language_hinglish():
    res = detect_language("AC kaam nahi kar raha B4 mein paani nahi hai")
    assert res["language"] == "Hinglish"
    assert res["is_multilingual"] is True


def test_detect_language_hindi_unicode():
    res = detect_language("एसी काम नहीं कर रहा है")
    assert res["language"] == "Hindi"
    assert res["is_multilingual"] is True


def test_normalize_multilingual_text_preserves_entities():
    res = normalize_multilingual_text("AC kaam nahi kar raha B4 seat 21 on train 12951")
    assert "B4" in res["normalized_text"]
    assert "21" in res["normalized_text"]
    assert "12951" in res["normalized_text"]
    assert res["is_multilingual"] is True
