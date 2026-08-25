import os
import sys

# Ensure repository root, app, and frontend directories are on sys.path for pytest
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
APP_DIR = os.path.join(ROOT_DIR, "app")
FRONTEND_DIR = os.path.join(APP_DIR, "frontend")

for path in [ROOT_DIR, APP_DIR, FRONTEND_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)
