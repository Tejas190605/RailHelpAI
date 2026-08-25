import os
import csv
import json
import random
from datetime import datetime, timedelta, timezone

# Fix random seed for strict reproducibility
SEED = 42
random.seed(SEED)

CATEGORIES = [
    "Air Conditioning", "Cleanliness", "Water Supply", "Electrical",
    "Catering", "Security", "Staff Behaviour", "Coach Maintenance",
    "Station Facilities", "Ticketing", "Medical", "Luggage",
    "Pest Control", "Other"
]

SUBCATEGORIES = {
    "Air Conditioning": ["AC Not Cooling", "AC Power Failure", "AC Temperature Too Low", "AC Water Leakage", "AC Noise"],
    "Cleanliness": ["Toilet Dirty", "Coach Floor Dirty", "Dustbin Overflowing", "Bedroll Unclean", "Window Dirty"],
    "Water Supply": ["No Water in Toilet", "Tap Water Leakage", "Drinking Water Supply", "Washbasin Blocked"],
    "Electrical": ["Charging Socket Broken", "Fan Not Working", "Light Switch Damaged", "Reading Light Blown"],
    "Catering": ["Food Quality Poor", "Food Cold / Stale", "Overcharging for Food", "Pantry Staff Rude", "Meal Not Served"],
    "Security": ["Unauthorized Passengers", "Theft of Belongings", "Harassment", "Smoking in Coach", "Luggage Security"],
    "Staff Behaviour": ["Rude TTE", "Attendant Absent", "Unhelpful Pantry Staff", "Misbehavior by Cleaning Staff"],
    "Coach Maintenance": ["Seat Broken / Loose", "Window Blind Jammed", "Door Lock Broken", "Emergency Chain Damaged"],
    "Station Facilities": ["Escalator Faulty", "Platform Cleanliness", "Waiting Room Dirty", "PA System Unclear"],
    "Ticketing": ["PNR Status Issue", "Ticket Counter Rush", "Refund Not Processed", "TC Fine Dispute"],
    "Medical": ["First Aid Required", "Passenger Ill", "Doctor Required", "Emergency Assistance"],
    "Luggage": ["Luggage Space Full", "Overweight Fine Dispute", "Parcel Delay"],
    "Pest Control": ["Cockroaches in Coach", "Rats Under Seat", "Mosquitoes / Bedbugs"],
    "Other": ["General Query", "Train Delay Complaint", "Noise Disturbance"]
}

STATIONS = [
    "Mumbai Central", "Pune Junction", "Thane", "Nashik Road", "Ahmedabad Junction",
    "Surat", "Vadodara Junction", "New Delhi", "Howrah Junction", "Chennai Central",
    "Bengaluru City", "Hyderabad Deccan", "Nagpur", "Jaipur Junction", "Lucknow Charbagh"
]

TRAINS = [
    ("12951", "Rajdhani Express"),
    ("12952", "New Delhi Rajdhani"),
    ("12137", "Punjab Mail"),
    ("12261", "Howrah Duronto"),
    ("12626", "Kerala Express"),
    ("12903", "Golden Temple Mail"),
    ("11020", "Konark Express"),
    ("12724", "Telangana Express"),
    ("12839", "Howrah Mail"),
    ("16346", "Netravati Express")
]

COACH_TYPES = ["B1", "B2", "B3", "B4", "B5", "A1", "A2", "S1", "S2", "S3", "S4", "S5", "HA1"]

TEMPLATES = {
    "Air Conditioning": [
        "AC is not cooling in coach {coach} seat {seat}. We have been waiting since {station}.",
        "Air conditioner has completely stopped working in coach {coach}. It is suffocating inside.",
        "AC temperature is too low in coach {coach} and heater isn't working.",
        "Water leaking from AC vent near seat {seat} in {coach}.",
        "AC in coach {coach} seat {seat} making loud noise and not cooling properly.",
        "No AC cooling in {coach}. Passengers are feeling sick since {station}."
    ],
    "Cleanliness": [
        "Toilet in coach {coach} is extremely dirty and smelling bad since {station}.",
        "Coach {coach} floor hasn't been cleaned since morning. Trash everywhere.",
        "Dustbin near gate in coach {coach} is overflowing and garbage is spilling.",
        "Unclean bedroll provided in coach {coach} berth {seat}. Please replace immediately.",
        "Washbasin in coach {coach} is full of dirt and blocked near seat {seat}."
    ],
    "Water Supply": [
        "No water supply in toilets of coach {coach}. Please refill at next station.",
        "Tap is leaking continuously in coach {coach} toilet near seat {seat}.",
        "No water in washbasin of coach {coach} since leaving {station}.",
        "Toilet water tank empty in coach {coach}. Passengers facing severe problem."
    ],
    "Electrical": [
        "Charging socket at seat {seat} in coach {coach} is broken and sparks are coming out.",
        "Fan above seat {seat} in coach {coach} is not working.",
        "Reading light near berth {seat} in {coach} is blown out.",
        "Main lights in coach {coach} not working since {station}."
    ],
    "Catering": [
        "Food served in coach {coach} seat {seat} was cold and stale.",
        "Pantry staff overcharging for water bottle and lunch meal in coach {coach}.",
        "Breakfast not served even after 3 hours of departure from {station}.",
        "Quality of dinner provided in train {train_number} coach {coach} was very poor."
    ],
    "Security": [
        "Unauthorized persons entered coach {coach} and harassing passengers near seat {seat}.",
        "My bag was stolen near seat {seat} in coach {coach} after {station}.",
        "Someone is smoking in the vestibule near coach {coach}. Please send RPF.",
        "Safety concern in coach {coach} as suspicious person wandering without ticket."
    ],
    "Staff Behaviour": [
        "TTE in coach {coach} was extremely rude when asked about seat {seat} allocation.",
        "Coach attendant in {coach} refused to assist senior citizen passenger at seat {seat}.",
        "Pantry vendor misbehaved with passengers near coach {coach}."
    ],
    "Coach Maintenance": [
        "Seat cushion at berth {seat} in coach {coach} is torn and loose.",
        "Window blind jammed in coach {coach} seat {seat}.",
        "Door lock of coach {coach} is damaged and shaking continuously."
    ],
    "Station Facilities": [
        "Escalator at platform near {station} is out of order.",
        "Waiting room at {station} is extremely dirty and fans are off.",
        "PA announcement system at {station} is completely distorted and unclear."
    ],
    "Ticketing": [
        "PNR status showing RAC but TTE denied berth in coach {coach}.",
        "Overcharged for ticket upgrade at {station} commercial counter.",
        "Refund for cancelled ticket not credited yet."
    ],
    "Medical": [
        "Medical emergency in coach {coach} seat {seat}. Passenger has high fever and chest pain.",
        "First aid needed urgently in coach {coach} near seat {seat} for injured child.",
        "Elderly passenger at seat {seat} in coach {coach} requires doctor assistance at {station}."
    ],
    "Luggage": [
        "Passenger at seat {seat} in coach {coach} blocking aisle with oversized luggage.",
        "Luggage space under seat {seat} in {coach} occupied by unauthorized bags."
    ],
    "Pest Control": [
        "Huge rats roaming under seat {seat} in coach {coach}. Please do pest control.",
        "Cockroaches found inside bedroll packet in coach {coach} seat {seat}.",
        "Bedbugs biting passengers in berth {seat} of coach {coach}."
    ],
    "Other": [
        "Train delayed by over 4 hours without any notification at {station}.",
        "Loud music playing in coach {coach} disturbing sleeping passengers near seat {seat}."
    ]
}

# Hinglish variations to mix into dataset
HINGLISH_VARIATIONS = [
    "AC bilkul thanda nahi kar raha coach {coach} seat {seat} me.",
    "Toilet me paani nahi aa raha in coach {coach} since {station}.",
    "Safai waala nahi aaya coach {coach} me garbage phaila hua hai.",
    "Pantry waala extra paise le raha hai food ke liye in coach {coach}.",
    "Coach {coach} seat {seat} ka fan band pad gaya hai garmi bohot hai.",
    "Rats ghoom rahe hai seat {seat} ke neeche coach {coach} me, pest control karo."
]


def generate_complaint_record(idx: int):
    category = random.choice(CATEGORIES)
    subcategory = random.choice(SUBCATEGORIES[category])
    train_num, train_name = random.choice(TRAINS)
    station = random.choice(STATIONS)
    coach = random.choice(COACH_TYPES)
    seat = str(random.randint(1, 72))

    # Decide if complaint is Hinglish
    is_hinglish = (random.random() < 0.15) and (category in ["Air Conditioning", "Cleanliness", "Water Supply", "Catering", "Electrical", "Pest Control"])
    
    if is_hinglish:
        template = random.choice(HINGLISH_VARIATIONS)
        text = template.format(coach=coach, seat=seat, station=station)
    else:
        template = random.choice(TEMPLATES[category])
        text = template.format(coach=coach, seat=seat, station=station, train_number=train_num)

    # Add typos occasionally
    if random.random() < 0.10:
        text = text.replace("cooling", "klning").replace("dirty", "drty").replace("working", "wrking")

    # Priority logic
    if category in ["Medical", "Security"]:
        priority = "P1"
    elif category in ["Air Conditioning", "Water Supply"]:
        priority = random.choice(["P1", "P2"])
    elif category in ["Cleanliness", "Electrical", "Catering"]:
        priority = random.choice(["P2", "P3"])
    else:
        priority = random.choice(["P3", "P4"])

    department_map = {
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
    department = department_map[category]

    sentiments = ["Positive", "Neutral", "Concerned", "Negative", "Angry", "Critical"]
    if priority == "P1":
        sentiment = random.choice(["Angry", "Critical"])
    elif priority == "P2":
        sentiment = random.choice(["Negative", "Angry", "Concerned"])
    else:
        sentiment = random.choice(["Neutral", "Concerned", "Negative"])

    status = random.choice(["New", "In Progress", "Resolved", "Escalated"])
    created_dt = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
    
    resolved_dt = ""
    res_time_min = ""
    if status == "Resolved":
        duration_minutes = random.randint(15, 480)
        resolved_dt = (created_dt + timedelta(minutes=duration_minutes)).isoformat()
        res_time_min = duration_minutes

    return {
        "complaint_id": f"RAI-SYN-{idx:05d}",
        "complaint_text": text,
        "category": category,
        "subcategory": subcategory,
        "train_number": train_num,
        "train_name": train_name,
        "station": station,
        "coach": coach,
        "seat": seat,
        "priority": priority,
        "department": department,
        "sentiment": sentiment,
        "status": status,
        "created_at": created_dt.isoformat(),
        "resolved_at": resolved_dt,
        "resolution_time": res_time_min
    }


def generate_dataset(num_records=10000, output_csv="data/synthetic/synthetic_complaints_10k.csv"):
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    records = [generate_complaint_record(i + 1) for i in range(num_records)]

    fieldnames = list(records[0].keys())
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"[SUCCESS] Generated {num_records} synthetic complaints in {output_csv}")


if __name__ == "__main__":
    generate_dataset()
