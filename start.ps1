# Trademind Jyotish OS - Hardened Windows Launcher (V1.0.0)
$ErrorActionPreference = "Stop"

# 1. Path Setup
$ProjectRoot = "D:\ASTROLOGYPREDICTIONS"
Set-Location $ProjectRoot

# 2. Virtual Environment Detection
$VenvPython = Join-Path $ProjectRoot "venv\Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    Write-Error "CRITICAL: Virtual environment not found at $VenvPython. Please run 'python -m venv venv' first."
    exit 1
}

# 3. Environment Variable Configuration
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item .env.example .env
        Write-Host "[INFO] Created .env from .env.example" -ForegroundColor Cyan
    }
}

# Load variables from .env
if (Test-Path ".env") {
    Get-Content .env | Where-Object { $_ -match "^(?<name>[^#\s].*?)=(?<value>.*)$" } | ForEach-Object {
        $name = $Matches['name'].Trim()
        $value = $Matches['value'].Trim()
        [System.Environment]::SetEnvironmentVariable($name, $value, "Process")
    }
}

# 4. Mandatory Security Check
if (-not $env:FLASK_SECRET_KEY -or $env:FLASK_SECRET_KEY -eq "CHANGE_ME_TO_RANDOM_HEX") {
    Write-Error "CRITICAL: FLASK_SECRET_KEY must be set in .env to start the application."
    exit 1
}

# 5. Runtime Environment
$env:PYTHONPATH = $ProjectRoot
$env:SE_EPHE_PATH = Join-Path $ProjectRoot "ephe"
$env:VIRTUAL_ENV = Join-Path $ProjectRoot "venv"
$env:PATH = "$(Join-Path $env:VIRTUAL_ENV 'Scripts');$env:PATH"

# 6. Start Application
Write-Host "------------------------------------------------" -ForegroundColor Gray
Write-Host "  🔮 Trademind Jyotish AI Dashboard (V1.0.0)" -ForegroundColor Yellow
Write-Host "  Engine: Swiss Ephemeris (Deterministic)" -ForegroundColor Yellow
Write-Host "------------------------------------------------" -ForegroundColor Gray
Write-Host "Starting Backend at http://localhost:5001..." -ForegroundColor Green

& $VenvPython run.py
