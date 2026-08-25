import pytest
from app.ai.entity_extractor import extract_entities


def test_extract_train_coach_seat_station():
    text = "The charging sockets in B4 seats 21 and 22 haven't worked since Pune on train 12951 for 30 minutes."
    entities = extract_entities(text)

    assert entities.get("train_number") == "12951"
    assert entities.get("coach") == "B4"
    assert entities.get("station") == "Pune"
    assert "21" in entities.get("seats", [])
    assert "22" in entities.get("seats", [])
    assert "30 minutes" in entities.get("duration", "")


def test_extract_empty_text():
    assert extract_entities("") == {}
