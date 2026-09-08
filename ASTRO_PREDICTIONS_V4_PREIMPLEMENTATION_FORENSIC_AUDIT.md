# ASTRO PREDICTIONS V4 PRE-IMPLEMENTATION FORENSIC AUDIT

## 1. Architecture Map
- **Frontend / Presentation**: Flask Jinja templates (`app/templates/dashboard.html`, `predictions.html`, `timeline.html`, `showcase.html`, `index.html`, `kundli.html`) adhering to a premium executive dark theme.
- **Backend Routing**: Flask Blueprint (`main` in `app/routes.py`) managing routes (`/`, `/dashboard`, `/predictions`, `/timeline`, `/showcase`, `/history`, `/kundli`).
- **Data Persistence**: SQLAlchemy ORM (`app/database/models.py`) with SQLite (`data/app.db`), storing `Profile`, `Chart`, and immutable `PredictionOutcome` snapshots.
- **Calculation Backend**: Isolated FastAPI calculation service (`calculation_service/app/main.py`) powered by Swiss Ephemeris (`pyswisseph`) for sidereal astronomical coordinates, house cusps, and transit ranges.
- **Prediction Engine (V3.15 Frozen)**: Domain-specific prediction engines (`app/astrology/predictions/engines/*`) synthesizing natal promise, Vimshottari dasha activation, and transit triggers into evidence-based confidence scores.

## 2. Calculation Map
- **Ayanamsa**: Lahiri (default), Raman, KP (via Swiss Ephemeris sidereal mode).
- **Planetary Calculations**: Topocentric longitudes, retrograde status, combustion, and speed (`swe.calc_ut`).
- **House Systems**: Whole Sign and Placidus via Swiss Ephemeris house calculation (`swe.houses_ex`).
- **Nakshatras**: 27 nakshatras divided into 4 padas (13°20' span per nakshatra, 3°20' per pada).
- **Dashas**: Multi-level Vimshottari Dasha calculation based on Moon's natal nakshatra placement.
- **Divisional Charts**: 16 Parashari Varga calculations (D1 to D60) in `app/astrology/charts/divisional.py`.
- **Yogas & Strength**: Rule-based classical yoga detection and Ashtakavarga / Shadbala calculation models.

## 3. Prediction & Timing Map
- **Scoring**: Internal confluence scoring (0–100 scale) based on multi-factor corroboration across natal promise, dasha activation, and transit triggers.
- **Timing Windows**: Active window (build/decline) and deterministic peak calculation from transit-dasha confluence.
- **Why Now**: Endpoint `/api/v1/predict/explain/<domain>` returning hierarchical evidence chains (Natal Promise, Dasha Activation, Transit Trigger, Divisional Confirmation).

## 4. Hardcoded Data & Test Fixture Map
- **Test Fixtures**: `Subramanian T S` and `GateV323` used as verified test fixtures for A/B/A validation.
- **Production Data**: Dynamically generated from user-submitted birth data (`dob`, `tob`, `place`, `lat`, `lon`, `tz`). Zero hardcoded production intelligence.

## 5. Weaknesses & Target Areas for V4 Upgrade
- **Confidence Calibration**: Moving beyond internal signal scores to statistically calibrated confidence intervals.
- **Contradiction Resolution**: Deepening the net-evidence model to explicitly weigh conflicting planetary influences.
- **Backtesting Lab**: Expanding automated precision/recall evaluation against historical datasets.
