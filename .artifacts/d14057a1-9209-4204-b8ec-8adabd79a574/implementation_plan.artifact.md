# Implementation Plan: Fix Cloud 503 Service Unavailable

The application is returning a 503 error on Google Cloud Run. This is likely due to a `NameError` in `app/routes.py` and a potential startup crash in the Firestore client initialization.

## User Review Required

> [!IMPORTANT]
> These changes are critical for the application to start in a serverless environment. No architectural changes are made, only bug fixes and robustness improvements.

## Proposed Changes

### 1. Route Import Fixes

#### [MODIFY] [routes.py](file:///G:/Astrology%20Prediction/app/routes.py)
- Add `import pytz` to the top-level imports.
- Ensure all helper functions have necessary imports.

### 2. Firestore Robustness

#### [MODIFY] [firebase_store.py](file:///G:/Astrology%20Prediction/app/astrology/firebase_store.py)
- Move `firestore.Client()` initialization inside a helper function `_get_db()` to avoid top-level execution during module import.

### 3. Database Initialization Fix

#### [MODIFY] [__init__.py](file:///G:/Astrology%20Prediction/app/__init__.py)
- Ensure the app context and database initialization are isolated to prevent crashes in read-only environments.

## Verification Plan

### Automated Tests
- I will run a local startup test to ensure no `ImportError` or `NameError` occurs.

### Manual Verification
- The user will need to redeploy using the provided scripts.
