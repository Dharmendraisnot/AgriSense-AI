# AgriSense AI – Run Instructions
# ================================
# PowerShell script to start both the FastAPI backend and Streamlit frontend.
# Run from the project root:
#   .\run.ps1

Write-Host "🌾 Starting AgriSense AI..." -ForegroundColor Green

# ── Install dependencies if needed ──────────────────────────
if (-not (Test-Path ".\venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate venv
. ".\venv\Scripts\Activate.ps1"

# ── Start FastAPI backend (background job) ───────────────────
Write-Host "🚀 Starting FastAPI backend on http://localhost:8000 ..." -ForegroundColor Cyan
$backend = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    & .\venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
}

Start-Sleep -Seconds 3

# ── Start Streamlit frontend ─────────────────────────────────
Write-Host "🌐 Starting Streamlit frontend on http://localhost:8501 ..." -ForegroundColor Cyan
streamlit run frontend/app.py

# Cleanup on exit
Stop-Job $backend
Remove-Job $backend
