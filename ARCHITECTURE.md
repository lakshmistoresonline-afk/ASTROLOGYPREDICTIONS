# ASTROLOGYPREDICTIONS Architecture

## 🏛️ Deterministic Inference Chain
The application follows a strictly tiered pipeline to ensure every life insight is derived from calculated facts rather than generic text or random generation.

`CALCULATION → ASTROLOGICAL FACTS → STRENGTH ANALYSIS → YOGAS → VARGAS → DASHA → TRANSITS → DOMAIN ANALYSIS → EVENT DETECTION → TIMING → CONTRADICTION ANALYSIS → CONFIDENCE → EXPLANATION → AI NARRATIVE`

## 🧱 Core Components

### 1. Calculation Engine (`app/astrology/core/`)
- **Swiss Ephemeris (`pyswisseph`)**: Used for high-precision planetary positions.
- **Topocentric Precision**: Settings are enabled to account for latitude and longitude.
- **Lahiri Ayanamsa**: Default sidereal calculation standard.
- **Canonical Model (`models.py`)**: Central `CanonicalChart` object used by all predictors.

### 2. Strength & Yoga Engines (`app/astrology/strength/`, `app/astrology/yogas/`)
- **Shadbala**: Implements all 6 traditional components of planetary strength.
- **Varga Engine**: Supports all 16 divisional charts (D1 to D60) with Parashari rules.
- **Yoga Detector**: Detects 100+ standard yogas (Rajayoga, Dhana, Nabhasa, etc.).

### 3. Timing & Transit Engines (`app/astrology/timing/`, `app/astrology/transit/`)
- **Vimshottari Dasha**: Multi-level dasha calculation (Maha, Antar, Pratyantar).
- **Ashtakavarga (SAV)**: Integrated into timing to weight transit impact.
- **TimingEngine**: Synthesizes natal potential with current dasha and transit support.

### 4. Prediction Engine (`app/astrology/predictions/`)
- **EvidenceEngine**: Standardizes facts into weighted evidence objects.
- **ContradictionEngine**: Analyzes conflicting signals between natal and varga charts.
- **Domain Modules**: 38+ specialized modules for Personality, Career, Wealth, etc.

## 🛡️ Security
- **Mandatory Secrets**: `FLASK_SECRET_KEY` is enforced from environment variables.
- **Secure Headers**: HSTS, CSP, and X-Frame-Options are configured in production.

## 🧪 Testing
- **Regression Suite**: `tests/regression/` uses golden charts to verify calculation integrity.
- **Unit Tests**: Coverage for individual astrology algorithms (Vargas, Yogas).
