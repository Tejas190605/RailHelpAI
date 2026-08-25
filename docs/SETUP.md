# RailHelpAI — Local Setup & Reproducibility Guide

> **Version:** v1.0 (Phase 6 Final Release)  

---

## 1. Prerequisites
- Python 3.10+ (Tested on Python 3.14 on Windows 11)
- Git

---

## 2. One-Command Setup Workflow

```powershell
# 1. Clone repository
git clone https://github.com/Tejas190605/RailHelpAI.git
cd RailHelpAI

# 2. Create virtual environment & install dependencies
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Initialize fresh SQLite database & seed demo data
python app/database/init_db.py
python scripts/seed_demo_data.py

# 4. Start FastAPI Backend (Port 8000)
.\scripts\start_backend.ps1

# 5. In a second terminal, start Streamlit Frontend (Port 8501)
.\scripts\start_frontend.ps1
```

Access application at: `http://127.0.0.1:8501`
