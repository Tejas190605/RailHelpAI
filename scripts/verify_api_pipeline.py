import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"


def verify_live_api():
    print("Testing live FastAPI backend endpoints...")
    
    # Health
    res = requests.get("http://127.0.0.1:8000/health")
    print(f"Health Status Code: {res.status_code}")
    print(f"Health Response: {res.json()}")

    # AI Analyze
    ai_payload = {
        "text": "AC is not cooling in coach B4 seat 21 and we have been waiting for 30 minutes since Pune on train 12951.",
        "train_number": "12951",
        "coach": "B4",
        "seat": "21",
        "station": "Pune"
    }
    res_ai = requests.post(f"{BASE_URL}/ai/analyze", json=ai_payload)
    print(f"\nAI Analyze Status Code: {res_ai.status_code}")
    print("AI Analyze Output:")
    print(json.dumps(res_ai.json(), indent=2))

    # Create Complaint (Auto AI Processing + DB Audit)
    complaint_payload = {
        "complaint_text": "Medical emergency in coach A1 seat 14. Passenger having chest pain.",
        "train_number": "12261",
        "coach": "A1",
        "seat": "14"
    }
    res_comp = requests.post(f"{BASE_URL}/complaints", json=complaint_payload)
    print(f"\nCreate Complaint Status Code: {res_comp.status_code}")
    print("Created Complaint Record:")
    print(json.dumps(res_comp.json(), indent=2))

    print("\nLive API Verification Completed Successfully!")


if __name__ == "__main__":
    verify_live_api()
