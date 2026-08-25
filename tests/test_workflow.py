import pytest
from app.services.workflow import validate_state_transition, get_allowed_next_states


def test_valid_state_transitions():
    assert validate_state_transition("NEW", "AI_ANALYZED") is True
    assert validate_state_transition("AI_ANALYZED", "ASSIGNED") is True
    assert validate_state_transition("ASSIGNED", "IN_PROGRESS") is True
    assert validate_state_transition("IN_PROGRESS", "RESOLVED") is True
    assert validate_state_transition("RESOLVED", "CLOSED") is True


def test_invalid_state_transitions():
    assert validate_state_transition("NEW", "RESOLVED") is False
    assert validate_state_transition("NEW", "CLOSED") is False
    assert validate_state_transition("RESOLVED", "IN_PROGRESS") is False
    assert validate_state_transition("CLOSED", "NEW") is False


def test_same_status_update_allowed():
    assert validate_state_transition("IN_PROGRESS", "IN_PROGRESS") is True


def test_get_allowed_next_states():
    states = get_allowed_next_states("IN_PROGRESS")
    assert "RESOLVED" in states
    assert "WAITING_FOR_INFORMATION" in states
