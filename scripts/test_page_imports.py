import os
import sys
import importlib

# Ensure sys.path matches app.py runtime environment
FRONTEND_DIR = os.path.abspath("app/frontend")
APP_DIR = os.path.abspath("app")
PROJECT_DIR = os.path.abspath(".")

for p in [FRONTEND_DIR, APP_DIR, PROJECT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

pages = [
    "pages.01_Overview",
    "pages.02_Submit_Complaint",
    "pages.03_AI_Analysis",
    "pages.04_Complaint_Queue",
    "pages.05_SLA_Monitor",
    "pages.06_Human_Review_Queue",
    "pages.07_Complaint_Detail",
    "pages.08_Train_Intelligence",
    "pages.09_Station_Intelligence",
    "pages.10_Incident_Clusters",
    "pages.11_Executive_Intelligence",
]

print("Testing page module imports...")
success = True
for page_module in pages:
    try:
        mod = importlib.import_module(page_module)
        print(f"  [PASS] {page_module}")
    except Exception as e:
        print(f"  [FAIL] {page_module}: {type(e).__name__}: {e}")
        success = False

if not success:
    sys.exit(1)
print("All 11 page modules imported successfully without errors!")
