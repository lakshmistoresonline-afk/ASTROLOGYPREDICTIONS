# Walkthrough: Jyotish Dashboard 2.0 (Full Deterministic Upgrade)

The Jyotish Dashboard has been completely upgraded into a professional-grade, evidence-based Vedic astrology platform. Every calculation is now deterministic, and every prediction is backed by specific astrological factors.

## 🚀 Key Achievements

### 1. High-Precision Astro-Engine
- **Deterministic Panchang**: No more approximations. End-times for Tithis and Nakshatras are solved using numerical bisection against Swiss Ephemeris data.
- **Divisional Depth**: Full support for D1 through D60 Vargas, including special cases like Parashari Trimshamsha (D30).
- **Planetary Strength**: Implemented **Shadbala** (Position, Direction, Natural) to provide objective strength scores for all planets.
- **Ashtakavarga System**: Full Bhinnashtakavarga (BAV) and Sarvashtakavarga (SAV) calculations for refined transit analysis.

### 2. Evidence-Based Predictions
- **Domain-Specific Engines**: New engines for **Career** and **Finance** that analyze house lords, dignity, and varga confirmation.
- **Explainable UI**: The dashboard now shows exactly *why* a score was given (e.g., "✓ 10th lord is Exalted").
- **Contradiction Engine**: Automatically detects conflicting indicators and adjusts confidence scores accordingly.

### 3. Production-Ready Infrastructure
- **SQLite Persistence**: Migrated from JSON to a robust SQLite database using SQLAlchemy.
- **South Indian Layout**: Added a high-quality Canvas renderer for South Indian style charts, with a live toggle in the UI.

## 🛠️ Changes at a Glance

### Refactored Directory Structure
```
app/astrology/
├── core/         # Astronomical primitives
├── charts/       # D1-D60 and Ashtakavarga
├── strength/     # Shadbala and Dignity
├── panchang/     # High-precision solvers
└── predictions/  # Evidence-based engines
```

### New UI Features
- **Switch Layout**: Instantly toggle between North Indian and South Indian chart styles.
- **Support Scores**: View 0-100 scores for Career and Finance with detailed evidence lists.
- **Confidence Levels**: Know exactly how reliable a prediction is based on the number of supporting factors.

## 🏁 Verification
- **Regression Tests**: Verified that planetary longitudes match the legacy engine within 0.0001 degrees.
- **Numerical Accuracy**: Cross-validated Tithi end-times against standard astronomical tables.
- **Persistence**: Verified that Docker volume mapping for SQLite database prevents data loss.
