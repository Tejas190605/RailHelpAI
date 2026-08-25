import re
from typing import Dict, Any, List, Optional


def extract_entities(text: str) -> Dict[str, Any]:
    """
    Extract structured operational entities from natural language complaint text
    using regular expressions and keyword pattern matching.
    """
    if not text or not isinstance(text, str):
        return {}

    entities = {}

    # Extract Train Number (e.g. 12951, 12261)
    train_match = re.search(r"\b(\d{5})\b", text)
    if train_match:
        entities["train_number"] = train_match.group(1)

    # Extract Coach Code (e.g., B4, S2, HA1, A1, H1, D1)
    coach_match = re.search(r"\b([A-Za-z]{1,2}\d{1,2})\b", text)
    if coach_match:
        coach_val = coach_match.group(1).upper()
        # Ensure it matches standard coach patterns (e.g. B1-B12, S1-S12, A1-A4, H1, HA1, D1-D5)
        if re.match(r"^(B|S|A|H|HA|D|G|E|M)\d{1,2}$", coach_val):
            entities["coach"] = coach_val

    # Extract Seat / Berth numbers (e.g. seat 21, berth 42, seats 21 and 22)
    seat_matches = re.findall(r"\b(?:seat|berth|seats|berths)\s*(?:nos?\.?)?\s*(\d{1,2})(?:\s*(?:and|&|,)\s*(\d{1,2}))?\b", text, re.IGNORECASE)
    seats = []
    if seat_matches:
        for match in seat_matches:
            for seat_num in match:
                if seat_num and seat_num not in seats:
                    seats.append(seat_num)
    else:
        # Fallback single seat match
        single_seat = re.search(r"\b(\d{1,2})\b", text)
        if single_seat and "coach" in entities:
            seat_val = single_seat.group(1)
            # Exclude train number match if identical
            if seat_val != entities.get("train_number"):
                seats.append(seat_val)

    if seats:
        entities["seats"] = seats
        entities["seat"] = seats[0]

    # Extract Duration (e.g., 30 minutes, 2 hours, 3 hrs)
    duration_match = re.search(r"\b(\d+\s*(?:mins?|minutes?|hrs?|hours?))\b", text, re.IGNORECASE)
    if duration_match:
        entities["duration"] = duration_match.group(1)

    # Extract Known Stations / Location
    stations = [
        "Mumbai Central", "Pune", "Thane", "Nashik", "Ahmedabad",
        "Surat", "Vadodara", "New Delhi", "Howrah", "Chennai",
        "Bengaluru", "Hyderabad", "Nagpur", "Jaipur", "Lucknow"
    ]
    for st in stations:
        if re.search(rf"\b{st}\b", text, re.IGNORECASE):
            entities["station"] = st
            entities["location"] = st
            break

    # Extract Issue keyphrase
    lower_text = text.lower()
    if "ac" in lower_text:
        entities["issue"] = "AC Malfunction / Cooling Issue"
    elif "water" in lower_text:
        entities["issue"] = "Water Supply Issue"
    elif "clean" in lower_text or "dirty" in lower_text or "toilet" in lower_text:
        entities["issue"] = "Cleanliness / Housekeeping Issue"
    elif "socket" in lower_text or "fan" in lower_text or "light" in lower_text:
        entities["issue"] = "Electrical Issue"
    elif "food" in lower_text or "pantry" in lower_text or "meal" in lower_text:
        entities["issue"] = "Catering / Food Quality"
    elif "stolen" in lower_text or "theft" in lower_text or "smoke" in lower_text:
        entities["issue"] = "Security / Theft Issue"
    elif "medical" in lower_text or "doctor" in lower_text or "fever" in lower_text:
        entities["issue"] = "Medical Emergency"
    elif "rat" in lower_text or "cockroach" in lower_text or "bug" in lower_text:
        entities["issue"] = "Pest Control Issue"

    return entities
