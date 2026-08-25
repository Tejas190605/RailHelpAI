# Dataset Documentation — RailHelpAI Synthetic Complaints

## Dataset Overview
- **File Path:** `data/synthetic/synthetic_complaints_10k.csv`
- **Record Count:** 10,000 complaints
- **Generation Method:** Reproducible Python generator script (`scripts/generate_synthetic_data.py`) with fixed seed (`seed=42`).
- **Privacy Assurance:** 100% synthetic/anonymized data; zero real PII, zero real PNRs, zero real passenger details.

## Target Categories (14 Classes)
1. Air Conditioning
2. Cleanliness
3. Water Supply
4. Electrical
5. Catering
6. Security
7. Staff Behaviour
8. Coach Maintenance
9. Station Facilities
10. Ticketing
11. Medical
12. Luggage
13. Pest Control
14. Other

## Dataset Fields
- `complaint_id`: Unique identifier (e.g. `RAI-SYN-00001`)
- `complaint_text`: Raw complaint text (English, typos, Hinglish)
- `category`: Ground truth category
- `subcategory`: Specific issue subcategory
- `train_number`: Train number (e.g., `12951`)
- `train_name`: Train name (e.g., `Rajdhani Express`)
- `station`: Nearest station
- `coach`: Coach code (e.g. `B4`, `S2`)
- `seat`: Seat / berth number
- `priority`: Assigned ground truth priority (`P1`, `P2`, `P3`, `P4`)
- `department`: Responsible department
- `sentiment`: Sentiment label
- `status`: Complaint status
- `created_at`: Creation timestamp
- `resolved_at`: Resolution timestamp
- `resolution_time`: Resolution duration in minutes
