import os
import sys
import runpy
from pathlib import Path

# Ensure sys.path matches app.py runtime environment
PROJECT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_DIR / "app" / "frontend"
APP_DIR = PROJECT_DIR / "app"

for p in [str(FRONTEND_DIR), str(APP_DIR), str(PROJECT_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

pages_dir = FRONTEND_DIR / "pages"
page_files = sorted([f for f in pages_dir.glob("*.py") if not f.name.startswith("__")])

print(f"Testing {len(page_files)} page module imports...")
success = True
for page_file in page_files:
    try:
        runpy.run_path(str(page_file))
        print(f"  [PASS] {page_file.name}")
    except Exception as e:
        print(f"  [FAIL] {page_file.name}: {type(e).__name__}: {e}")
        success = False

if not success:
    sys.exit(1)
print("All 11 page modules imported successfully without errors!")
