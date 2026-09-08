# Trademind Jyotish AI — Production Startup Script (V3.15)
# ═════════════════════════════════════════════════════════════════════════

Write-Host "🌟 TRADEMIND JYOTISH AI — PRODUCTION MODE" -ForegroundColor Cyan
Write-Host "Engine Version: V3.15 FROZEN" -ForegroundColor Yellow
Write-Host "Baseline: 60.7% Precision (Validated)" -ForegroundColor Gray
Write-Host "---------------------------------------------------------------"

# 1. Dependency Check
Write-Host "[1/4] Checking Dependencies..."
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python not found. Please install Python 3.10+."
    exit
}

# 2. Database Verification
Write-Host "[2/4] Verifying Database Schema..."
$env:PYTHONPATH="."
python scripts/v315_migrate_db.py
python scripts/v315_harden_db.py

# 3. Launch Calculation Service
Write-Host "[3/4] Starting Calculation Engine (Port 8000)..."
$CalcProc = Start-Process python -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 8000" -WorkingDirectory "calculation_service" -PassThru -WindowStyle Hidden

# Wait for readiness
Write-Host "      Warming up engine..."
$Ready = $false
for ($i=0; $i -lt 15; $i++) {
    try {
        $resp = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 1 -ErrorAction SilentlyContinue
        if ($resp.StatusCode -eq 200) { $Ready = $true; break }
    } catch {}
    Start-Sleep -Seconds 1
}

if (!$Ready) {
    Write-Error "Calculation Engine failed to start."
    $CalcProc | Stop-Process -Force
    exit
}
Write-Host "✅ Calculation Engine is ONLINE."

# 4. Launch Dashboard
Write-Host "[4/4] Starting Jyotish Dashboard (Port 5001)..."
Write-Host "---------------------------------------------------------------"
Write-Host "👉 Dashboard will open in your default browser."
Write-Host "👉 Use Ctrl+C to stop all services."
Write-Host "---------------------------------------------------------------"

try {
    python run.py
} finally {
    Write-Host "`n🛑 SHUTTING DOWN..."
    if ($CalcProc) { $CalcProc | Stop-Process -Force }
    Write-Host "👋 Goodbye."
}
