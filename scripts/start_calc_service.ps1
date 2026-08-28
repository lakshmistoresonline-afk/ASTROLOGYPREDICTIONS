# Launcher for isolated Calculation Service (without Docker)
$env:PYTHONPATH = "calculation_service"
Write-Host "Starting Isolated Calculation Service on http://localhost:8000" -ForegroundColor Cyan
uvicorn app.main:app --host 0.0.0.0 --port 8000
