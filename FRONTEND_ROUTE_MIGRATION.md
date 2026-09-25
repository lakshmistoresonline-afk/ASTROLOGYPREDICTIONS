# 🗺️ ASTRO PREDICTIONS — FRONTEND ROUTE MIGRATION MAP

## Overview
This document records the migration mapping from legacy Flask Jinja templates to the authoritative Next.js 14 / React 18 / TypeScript frontend routes.

---

## Route Migration Matrix

| Application Route | Legacy Flask Template | Authoritative Next.js Page | Backend API Endpoint | Auth Required | Migration Status |
|---|---|---|---|---|---|
| **`/login`** | `app/templates/login.html` | `frontend/src/pages/Login.tsx` | `POST /login` | NO (Public) | 🟢 **MIGRATED** |
| **`/` & `/dashboard`** | `app/templates/dashboard.html` | `frontend/src/pages/Dashboard.tsx` | `GET /api/v1/debug/dashboard-data` | YES | 🟢 **MIGRATED** |
| **`/profile/new`** | `app/templates/create_profile.html` | `frontend/src/pages/ProfileNew.tsx` | `POST /api/v3/predict/full` | YES | 🟢 **MIGRATED** |
| **`/kundli`** | `app/templates/kundli.html` | `frontend/src/pages/Kundli.tsx` | `POST /api/v3/predict/full` | YES | 🟢 **MIGRATED** |
| **`/predictions`** | `app/templates/predictions.html` | `frontend/src/pages/Predictions.tsx` | `GET /api/v1/predict/explain/<domain>` | YES | 🟢 **MIGRATED** |
| **`/timeline`** | `app/templates/timeline.html` | `frontend/src/pages/Timeline.tsx` | `GET /timeline` | YES | 🟢 **MIGRATED** |
| **`/transit`** | `app/templates/transit.html` | `frontend/src/pages/Transit.tsx` | `GET /api/transit/heatmap` | YES | 🟢 **MIGRATED** |
| **`/matchmaking`** | `app/templates/matchmaking.html` | `frontend/src/pages/Matchmaking.tsx` | `POST /matchmaking` | YES | 🟢 **MIGRATED** |
| **`/history`** | `app/templates/history.html` | `frontend/src/pages/History.tsx` | `GET /my-charts` | YES | 🟢 **MIGRATED** |
| **`/pricing`** | `app/templates/commercial/pricing.html` | `frontend/src/pages/Pricing.tsx` | `GET /commercial/pricing` | NO (Public) | 🟢 **MIGRATED** |
| **`/admin/accuracy`**| `app/templates/admin_accuracy.html` | `frontend/src/pages/admin/Accuracy.tsx` | `GET /admin/accuracy` | YES (Admin) | 🟢 **MIGRATED** |

---

## Next.js Proxy & Flask Integration Architecture
- **Development Server**: Next.js runs on `http://localhost:3000` with API rewrites proxying requests to Flask API on `http://127.0.0.1:5000`.
- **Production Bundle**: `python scripts/build_and_sync_frontend.py` compiles Next.js pages (`7/7 static pages`) and syncs output bundle directly to Flask static directory `app/static/frontend_bundle/`.
