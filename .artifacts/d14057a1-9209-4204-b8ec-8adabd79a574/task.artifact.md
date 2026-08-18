# Task List: Free-Tier Firebase & Cloud Migration

- [x] Astrological Fixes
    - [x] Correct Rahu Kaal and Yamaghanta weekday mappings in `calculator.py`
    - [x] Verify fixes (logic verified)
- [x] Database Migration
    - [x] Add `google-cloud-firestore` to `requirements.txt`
    - [x] Create `app/astrology/firebase_store.py` for Firestore integration
    - [x] Update `app/astrology/store.py` to support environment-based switching
- [x] Cloud Deployment Config
    - [x] Update `Dockerfile` for Cloud Run (slimmer image, bundled ephemeris)
    - [x] Create `firebase.json` for Hosting proxy
- [x] Documentation & Cleanup
    - [x] Update `README.md` with Cloud deployment instructions
    - [x] Create a `walkthrough.artifact.md`
