# RailHelpAI — PowerShell Frontend Startup Script
Write-Host "Starting RailHelpAI Streamlit Frontend Server on http://127.0.0.1:8501 ..." -ForegroundColor Green

if (Test-Path "venv\Scripts\python.exe") {
    .\venv\Scripts\python.exe -m streamlit run app/frontend/app.py --server.port 8501
} else {
    streamlit run app/frontend/app.py --server.port 8501
}
