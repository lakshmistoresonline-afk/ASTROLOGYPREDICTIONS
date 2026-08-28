# Trademind Jyotish OS - Windows Launcher (V1.0.0)

# Check for .env
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item .env.example .env
        Write-Host "Created .env from .env.example" -ForegroundColor Cyan
    }
}

# Enforce Secret Key
if (-not $env:FLASK_SECRET_KEY) {
    if (Test-Path ".env") {
        Get-Content .env | Where-Object { $_ -match "^FLASK_SECRET_KEY=(.+)" } | ForEach-Object {
            $env:FLASK_SECRET_KEY = $matches[1]
        }
    }
}

if (-not $env:FLASK_SECRET_KEY) {
    Write-Error "CRITICAL: FLASK_SECRET_KEY must be set in environment or .env file."
    exit 1
}

# Environment
$env:PYTHONPATH = "."
$env:SE_EPHE_PATH = "$PSScriptRoot\ephe"

Write-Host "Starting Jyotish OS Backend..." -ForegroundColor Green
python run.py
