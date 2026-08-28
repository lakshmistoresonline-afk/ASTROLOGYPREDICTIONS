# ══════════════════════════════════════════════════════════════════
#  Jyotish Vedic Dashboard — Cloud Deployment (PowerShell)
#  Project: astropredictions-ff47c
#  User:    srinathrajkiran007@gmail.com
# ══════════════════════════════════════════════════════════════════

$PROJECT_ID = "astropredictions-ff47c"
$ACCOUNT = "srinathrajkiran007@gmail.com"
$REGION = "us-central1"

# Blocker 11 Fix: Removed hardcoded SECRET_KEY. Ensure $env:FLASK_SECRET_KEY is set.
if (-not $env:FLASK_SECRET_KEY) {
    Write-Error "ERROR: FLASK_SECRET_KEY is not set. Aborting deployment."
    return
}
$SECRET_KEY = $env:FLASK_SECRET_KEY

Write-Host "`n[1/3] Authenticating with Google Cloud..." -ForegroundColor Cyan
gcloud auth login $ACCOUNT

Write-Host "`n[2/3] Deploying Backend to Cloud Run..." -ForegroundColor Cyan
gcloud run deploy jyotish-dashboard `
  --source . `
  --project $PROJECT_ID `
  --account $ACCOUNT `
  --set-env-vars "USE_FIREBASE=true,FLASK_SECRET_KEY=$SECRET_KEY" `
  --allow-unauthenticated `
  --region $REGION

Write-Host "`n[3/3] Deploying Frontend to Firebase Hosting..." -ForegroundColor Cyan
# Ensure you are logged into firebase with the same account
firebase login --reauth # This will prompt in browser
firebase deploy --only hosting --project $PROJECT_ID

Write-Host "`n🚀 Deployment Complete!" -ForegroundColor Green
Write-Host "Check: https://$PROJECT_ID.web.app" -ForegroundColor Yellow
