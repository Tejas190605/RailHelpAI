from typing import Dict, Any, List, Optional

# Configurable default weight matrix
DEFAULT_WEIGHTS = {
    "severity": 0.45,
    "safety_risk": 0.30,
    "passenger_impact": 0.15,
    "waiting_time": 0.10
}


def calculate_priority(
    category: str,
    text: str,
    entities: Dict[str, Any],
    sentiment: str,
    weights: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Calculate composite priority score (0-100), assign priority level (P1-P4),
    and generate explainable rationale bullet points.
    """
    w = weights if weights else DEFAULT_WEIGHTS
    lower_t = text.lower()
    reasons = []

    # 1. Severity Rating (0 to 100)
    severity = 40.0
    if category in ["Medical", "Security"]:
        severity = 95.0
        reasons.append(f"High severity category '{category}' requiring immediate emergency response.")
    elif category in ["Air Conditioning", "Water Supply"]:
        severity = 75.0
        reasons.append(f"Significant utility impairment ({category}).")
    elif category in ["Cleanliness", "Electrical", "Catering"]:
        severity = 55.0
        reasons.append(f"Standard operational grievance ({category}).")
    else:
        severity = 35.0
        reasons.append(f"Minor / general inquiry category ({category}).")

    # Adjust severity if entire coach/train is affected
    if "coach" in entities or any(kw in lower_t for kw in ["coach", "entire", "all passengers"]):
        severity = min(severity + 10.0, 100.0)

    # 2. Safety Risk Rating (0 to 100)
    safety_risk = 10.0
    if any(kw in lower_t for kw in ["spark", "fire", "chest pain", "bleeding", "emergency", "stolen", "thief", "assault", "harass"]):
        safety_risk = 90.0
        reasons.append("Safety / physical risk factors detected in text.")
    elif category == "Security":
        safety_risk = 80.0
        reasons.append("Security related complaint.")
    elif category == "Electrical" and "spark" in lower_t:
        safety_risk = 85.0
        reasons.append("Potential electrical hazard detected.")
    else:
        reasons.append("No immediate physical life-threatening safety risk detected.")

    # 3. Passenger Impact Rating (0 to 100)
    passenger_impact = 40.0
    if "seats" in entities and len(entities["seats"]) > 1:
        passenger_impact = 80.0
        reasons.append(f"Multiple passengers affected (Seats: {', '.join(entities['seats'])}).")
    elif any(kw in lower_t for kw in ["all", "everyone", "entire coach", "crowd"]):
        passenger_impact = 85.0
        reasons.append("Coach-wide passenger impact.")
    else:
        passenger_impact = 50.0

    # 4. Waiting Duration Rating (0 to 100)
    waiting_time = 30.0
    if "duration" in entities:
        dur_str = str(entities["duration"]).lower()
        if "hour" in dur_str or "hrs" in dur_str:
            waiting_time = 85.0
            reasons.append(f"Unresolved for extended duration ({dur_str}).")
        elif "min" in dur_str:
            digits = "".join(filter(str.isdigit, dur_str))
            if digits and int(digits) >= 30:
                waiting_time = 70.0
                reasons.append(f"Unresolved for over 30 minutes ({dur_str}).")
            else:
                waiting_time = 45.0
                reasons.append(f"Waiting duration reported ({dur_str}).")
    elif "waiting" in lower_t or "since" in lower_t:
        waiting_time = 60.0
        reasons.append("Passenger reported ongoing waiting duration.")

    # Sentiment contribution to rationale (does NOT dictate priority alone)
    if sentiment in ["Angry", "Critical"]:
        reasons.append(f"Passenger sentiment is {sentiment}.")

    # Calculate composite score
    score = (
        severity * w["severity"] +
        safety_risk * w["safety_risk"] +
        passenger_impact * w["passenger_impact"] +
        waiting_time * w["waiting_time"]
    )
    score = round(min(max(score, 0.0), 100.0), 1)

    # Priority classification assignment
    if score >= 80.0:
        level = "P1"
    elif score >= 55.0:
        level = "P2"
    elif score >= 35.0:
        level = "P3"
    else:
        level = "P4"

    return {
        "priority_level": level,
        "priority_score": score,
        "confidence": 0.88,
        "reasons": reasons
    }
