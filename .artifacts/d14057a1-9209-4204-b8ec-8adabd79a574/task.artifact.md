# Task List: Jyotish Dashboard 2.0 Completion

## Phase 2: Core Calculation Refactor (Expanded)
- [x] Create directory structure
- [x] Implement core modules (ephemeris, ayanamsa, datetime, planets, houses)
- [x] Implement all Divisional Charts (D1-D60) in `app/astrology/charts/divisional.py`
- [x] Implement Ashtakavarga in `app/astrology/charts/ashtakavarga.py`

## Phase 4: Strength & Aspects Engine (Expanded)
- [x] Functional Benefic/Malefic logic
- [x] Classical Graha Drishti
- [x] Dignity engine
- [x] Implement Shadbala (Progressive implementation)
    - [x] Sthana Bala
    - [x] Dig Bala
    - [x] Naisargika Bala

## Phase 5: Predictions & Evidence (Expanded)
- [x] Weighted scoring engine
- [x] Career domain evidence
- [x] Finance domain evidence (D2, 2nd/11th houses)
- [x] Contradiction Detection & Confidence scoring

## Phase 6: Persistence & Infrastructure
- [x] SQLite Database Models (`app/database/models.py`)
- [x] SQLAlchemy Integration
- [x] Migration script from JSON to SQLite

## Phase 7: Application Integration & UI
- [x] Switch `routes.py` to use new `calculate_chart_data`
- [x] Update templates to display Evidence and Confidence
- [x] Implement South Indian Chart layout (Canvas renderer update)
- [x] Create Deployment Scripts for `srinathrajiran007@gmail.com`
- [ ] Final verification and testing
