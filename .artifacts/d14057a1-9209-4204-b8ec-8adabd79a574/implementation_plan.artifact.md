# Implementation Plan: Free-Tier Firebase & Cloud Migration

This plan outlines the steps to migrate the Jyotish Dashboard to a cloud-hosted environment (Firebase + Google Cloud Run) while strictly adhering to **Free Tier** limits. It also includes "Quick Win" fixes for astrological calculation bugs discovered during the audit.

## User Review Required

> [!IMPORTANT]
> To use Firestore, you will need to create a Firebase project in the [Firebase Console](https://console.firebase.google.com/) and download a `service-account.json` file (or use Application Default Credentials if deploying to Cloud Run).

> [!WARNING]
> Moving to the cloud means data is no longer stored locally on your disk but in the Google Cloud (Firestore). This ensures your charts are accessible from any device but changes the "100% offline" nature for the cloud-deployed version.

## Open Questions

- Would you like to keep the local JSON storage as a fallback/option for local development, or fully switch to Firestore?
- Should I proceed with adding **South Indian Chart support** as part of this migration, or focus purely on the Cloud transition first?

## Proposed Changes

### 1. Astrological Fixes (Quick Wins)
Correct the Rahu Kaal and Yamaghanta part-mappings to ensure accurate inauspicious windows.

#### [MODIFY] [calculator.py](file:///G:/Astrology%20Prediction/app/astrology/calculator.py)
- Update `_rahu_kaal` mapping for Wed/Thu/Fri.
- Update `_yamaghanta` mapping for all weekdays.

### 2. Database Migration (Firestore)
Abstract the storage layer to support both Local JSON and Firestore.

#### [NEW] [firebase_store.py](file:///G:/Astrology%20Prediction/app/astrology/firebase_store.py)
- Implement `save_chart`, `list_charts`, and `delete_chart` using the `google-cloud-firestore` SDK.
#### [MODIFY] [store.py](file:///G:/Astrology%20Prediction/app/astrology/store.py)
- Add a toggle/config to switch between `LocalStore` and `FirestoreStore`.

### 3. Cloud Deployment Configuration

#### [MODIFY] [Dockerfile](file:///G:/Astrology%20Prediction/Dockerfile)
- Ensure all `ephe` files are correctly copied into the image.
- Optimize for a smaller image size (using `python:3.11-slim`).
#### [NEW] [firebase.json](file:///G:/Astrology%20Prediction/firebase.json)
- Configure Firebase Hosting to proxy `/` to the Cloud Run service.

## Verification Plan

### Automated Tests
- I will create a scratch script in `C:\Users\Acer\AppData\Local\Google\AndroidStudio2026.1.2\projects\astrology prediction.27cbfdb7\.artifacts\d14057a1-9209-4204-b8ec-8adabd79a574/scratch/verify_kaal.py` to verify the Rahu Kaal fixes against known standard tables.

### Manual Verification
- Verify that charts saved to Firestore appear in the dashboard list.
- Verify that the app starts correctly in a containerized environment with the bundled ephemeris files.
