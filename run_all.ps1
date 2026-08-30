# Trademind Jyotish OS - Master Unified Launcher (V1.0.0)
$ErrorActionPreference = "Stop"

$ProjectRoot = "D:\ASTROLOGYPREDICTIONS"
Set-Location $ProjectRoot

# Clean up any existing processes
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*ASTROLOGYPREDICTIONS*" } | Stop-Process -Force

# 1. Start Calculation Service (Background)
Write-Host "[1/2] Starting Calculation Service..." -ForegroundColor Cyan
$CalcJob = Start-Job -ScriptBlock {
    cd "D:\ASTROLOGYPREDICTIONS\calculation_service"
    $env:PYTHONPATH = "."
    ..\venv\Scripts\python.exe -m uvicorn app.main:app --port 8000 --no-access-log
}

# 2. Wait for Calc Service Health
Write-Host "Waiting for engine to warm up..." -ForegroundColor Gray
Start-Sleep -Seconds 5

# 3. Start Backend Dashboard (Foreground)
Write-Host "[2/2] Starting Jyotish Dashboard..." -ForegroundColor Yellow
Write-Host "URL: http://localhost:5001" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop all services." -ForegroundColor White

try {
    .\start.ps1
} finally {
    Write-Host "
Stopping all services..." -ForegroundColor Red
    Stop-Job $CalcJob
    Get-Job | Remove-Job -Force
    Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*ASTROLOGYPREDICTIONS*" } | Stop-Process -Force
}
