# Implementation Plan: Jyotish Dashboard 2.0 (Completion Phase)

This plan covers the implementation of the remaining deterministic astrology features and the integration of the modular engine into the live application.

## User Review Required

> [!IMPORTANT]
> **Database Migration**: We will migrate from `charts.json` to **SQLite**. Existing charts will be imported automatically on the first run of the new engine.

> [!WARNING]
> **Engine Switchover**: Switching the Flask routes to the new high-precision engine will result in slightly different (more accurate) timings for Dasha and Panchang.

## Proposed Changes

### 1. Strength & Ashtakavarga Engine
Implement the mathematical models for planetary and sign strength.

#### [NEW] [shadbala.py](file:///G:/Astrology%20Prediction/app/astrology/strength/shadbala.py)
- Implement Sthana Bala (Positional), Dig Bala (Directional), Kala Bala (Temporal), and Cheshta Bala (Mototional).
- Normalize scores to a 0-100 scale for the prediction engine.
#### [NEW] [ashtakavarga.py](file:///G:/Astrology%20Prediction/app/astrology/charts/ashtakavarga.py)
- Implement Bhinnashtakavarga (BAV) for all 7 planets.
- Implement Sarvashtakavarga (SAV) for sign-level transit modification.

### 2. Expanded Predictions & Contradiction Detection
Increase the depth and reliability of the evidence-based engine.

#### [NEW] [finance.py](file:///G:/Astrology%20Prediction/app/astrology/predictions/finance.py)
- Analyze 2nd and 11th houses, their lords, and D2 (Hora) chart.
#### [MODIFY] [engine.py](file:///G:/Astrology%20Prediction/app/astrology/predictions/engine.py)
- Implement a **Contradiction Engine** that detects conflicting indicators (e.g., strong house lord but weak Shadbala) and adjusts the confidence score.

### 3. Production Persistence (SQLite)
Replace the JSON file store with a robust relational database.

#### [NEW] [models.py](file:///G:/Astrology%20Prediction/app/database/models.py)
- Define `Chart` and `Profile` models using SQLAlchemy.
#### [NEW] [migrate_json.py](file:///G:/Astrology%20Prediction/scripts/migrate_json.py)
- A one-time utility to move data from `data/charts.json` to `data/app.db`.

### 4. Application Integration
Finalize the transition to the 2.0 architecture.

#### [MODIFY] [routes.py](file:///G:/Astrology%20Prediction/app/routes.py)
- Replace legacy imports with the new modular structure.
- Update `/kundli` and `/predictions` endpoints to utilize the evidence-based results.

## Verification Plan

### Automated Tests
- `pytest tests/test_shadbala.py`: Validate strength calculations against standard manual examples.
- `pytest tests/test_migration.py`: Ensure data integrity during JSON to SQLite transition.

### Manual Verification
- Verify that the "Evidence" panel in the UI correctly displays the new factors from Shadbala and Ashtakavarga.
- Confirm that saved charts persist across application restarts.
