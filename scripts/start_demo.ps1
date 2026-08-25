# RailHelpAI — One-Command Demo Launcher Script
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "    RailHelpAI — One-Command Demo Launcher" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$pythonExe = if (Test-Path "venv\Scripts\python.exe") { ".\venv\Scripts\python.exe" } else { "python" }

Write-Host "Step 1: Initializing SQLite database schema..." -ForegroundColor Yellow
& $pythonExe app/database/init_db.py

Write-Host "Step 2: Seeding controlled demo scenarios..." -ForegroundColor Yellow
& $pythonExe scripts/seed_demo_data.py

Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "RailHelpAI platform initialized successfully!" -ForegroundColor Green
Write-Host "  Backend API:      http://127.0.0.1:8000" -ForegroundColor White
Write-Host "  Swagger Docs:     http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "  Streamlit Shell:  http://127.0.0.1:8501" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Green

Write-Host "`nTo run the platform services:" -ForegroundColor Cyan
Write-Host "  Terminal 1 (Backend):  .\scripts\start_backend.ps1" -ForegroundColor Gray
Write-Host "  Terminal 2 (Frontend): .\scripts\start_frontend.ps1" -ForegroundColor Gray
