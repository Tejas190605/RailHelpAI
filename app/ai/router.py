from typing import Dict, Any, Optional

# Single source of truth department routing table
DEPARTMENT_MATRIX = {
    "Air Conditioning": "Electrical / Coach Maintenance",
    "Cleanliness": "Housekeeping / Sanitation",
    "Water Supply": "Water Operations",
    "Electrical": "Electrical Maintenance",
    "Catering": "Catering Services",
    "Security": "Railway Protection Force (RPF)",
    "Staff Behaviour": "Passenger Grievance Cell",
    "Coach Maintenance": "Mechanical Engineering",
    "Station Facilities": "Station Administration",
    "Ticketing": "Ticketing & Commercial",
    "Medical": "Medical Emergency Response",
    "Luggage": "Luggage & Parcel Office",
    "Pest Control": "Pest Control Division",
    "Other": "General Operations"
}


def route_department(
    category: str,
    text: str = "",
    entities: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Route complaint to responsible department using centralized matrix and context rules.
    Returns department name, routing confidence, and routing rationale.
    """
    department = DEPARTMENT_MATRIX.get(category, "General Operations")
    confidence = 0.90
    reason = f"Routed to '{department}' based on category classification '{category}'."

    # Contextual overrides
    lower_t = text.lower() if text else ""
    if "rpf" in lower_t or "theft" in lower_t or "police" in lower_t:
        department = "Railway Protection Force (RPF)"
        confidence = 0.95
        reason = "Override to RPF based on explicit security/police keywords."
    elif "doctor" in lower_t or "ambulance" in lower_t or "chest pain" in lower_t:
        department = "Medical Emergency Response"
        confidence = 0.95
        reason = "Override to Medical Emergency Response based on medical indicators."

    return {
        "department": department,
        "routing_confidence": round(confidence, 2),
        "routing_reason": reason
    }
