from typing import List, Dict, Set

VALID_STATUSES: Set[str] = {
    "NEW",
    "AI_ANALYZED",
    "PENDING_REVIEW",
    "ASSIGNED",
    "IN_PROGRESS",
    "WAITING_FOR_INFORMATION",
    "RESOLVED",
    "CLOSED"
}

ALLOWED_TRANSITIONS: Dict[str, Set[str]] = {
    "NEW": {"AI_ANALYZED", "PENDING_REVIEW", "ASSIGNED"},
    "AI_ANALYZED": {"PENDING_REVIEW", "ASSIGNED"},
    "PENDING_REVIEW": {"ASSIGNED", "IN_PROGRESS"},
    "ASSIGNED": {"IN_PROGRESS", "WAITING_FOR_INFORMATION", "RESOLVED"},
    "IN_PROGRESS": {"WAITING_FOR_INFORMATION", "RESOLVED"},
    "WAITING_FOR_INFORMATION": {"IN_PROGRESS", "RESOLVED"},
    "RESOLVED": {"CLOSED"},
    "CLOSED": set()
}


def validate_state_transition(current_status: str, new_status: str) -> bool:
    """
    Validate if transition from current_status to new_status is allowed.
    Same-status updates are always allowed.
    """
    if current_status == new_status:
        return True

    curr_upper = current_status.upper().replace(" ", "_")
    new_upper = new_status.upper().replace(" ", "_")

    if curr_upper not in ALLOWED_TRANSITIONS:
        # Fallback for legacy state string compatibility
        return True

    return new_upper in ALLOWED_TRANSITIONS[curr_upper]


def get_allowed_next_states(current_status: str) -> List[str]:
    """Get list of allowed target statuses from current status."""
    curr_upper = current_status.upper().replace(" ", "_")
    return list(ALLOWED_TRANSITIONS.get(curr_upper, set()))
