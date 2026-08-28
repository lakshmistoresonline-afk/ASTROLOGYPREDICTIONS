#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════
#  Jyotish Vedic Dashboard — Cloud Deployment (Bash)
#  Project: astropredictions-ff47c
#  User:    srinathrajkiran007@gmail.com
# ══════════════════════════════════════════════════════════════════

PROJECT_ID="astropredictions-ff47c"
ACCOUNT="srinathrajkiran007@gmail.com"
REGION="us-central1"

# Blocker 11 Fix: Removed hardcoded SECRET_KEY. Ensure FLASK_SECRET_KEY is set in your environment.
if [ -z "$FLASK_SECRET_KEY" ]; then
    echo "ERROR: FLASK_SECRET_KEY is not set. Aborting deployment."
    exit 1
fi

echo -e "\n[1/3] Authenticating with Google Cloud..."
gcloud auth login $ACCOUNT

echo -e "\n[2/3] Deploying Backend to Cloud Run..."
gcloud run deploy jyotish-dashboard \
  --source . \
  --project $PROJECT_ID \
  --account $ACCOUNT \
  --set-env-vars "USE_FIREBASE=true,FLASK_SECRET_KEY=$SECRET_KEY" \
  --allow-unauthenticated \
  --region $REGION

echo -e "\n[3/3] Deploying Frontend to Firebase Hosting..."
firebase deploy --only hosting --project $PROJECT_ID

echo -e "\n🚀 Deployment Complete!"
echo -e "Check: https://$PROJECT_ID.web.app"
