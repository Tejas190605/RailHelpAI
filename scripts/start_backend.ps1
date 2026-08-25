# RailHelpAI — PowerShell Backend Startup Script
Write-Host "Starting RailHelpAI FastAPI Backend Server on http://127.0.0.1:8000 ..." -ForegroundColor Green

if (Test-Path "venv\Scripts\python.exe") {
    .\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
} else {
    python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
}
