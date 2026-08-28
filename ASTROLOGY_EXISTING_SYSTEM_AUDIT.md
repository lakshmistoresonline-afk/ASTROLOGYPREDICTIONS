# ASTROLOGYPREDICTIONS: Existing System Audit

## 1. Existing Architecture Summary

The current system is a **Python/Flask-based PWA (Progressive Web App)** that integrates astronomical calculations with multiple metaphysical systems. It uses a strictly tiered pipeline for processing, starting from deterministic calculations to AI-narrated interpretations.

-   **Backend:** Flask 3.0.3 with SQLAlchemy, Pydantic, and concurrent execution for prediction domains.
-   **Frontend:** HTML/CSS/JS (PWA) with a dashboard-centric UI.
-   **Calculation Engine:** `pyswisseph` (Swiss Ephemeris) wrapper with a mock fallback.
-   **Data Storage:** Local filesystem-based storage and optional Google Cloud Firestore.
-   **AI Integration:** Direct OpenAI/Ollama calls for chat and "Day Notes".

## 2. Component Audit

### A. Astrology Calculation Engine (`app/astrology/core/`)
-   **Real Calculations:** Uses Swiss Ephemeris for planetary longitudes, houses (Whole Sign by default), and basic divisional charts.
-   **Strengths:** Comprehensive implementation of Shadbala, Ashtakavarga, and Varga charts (D1-D60).
-   **Risks:** 
    -   **`swe_proxy.py` Mock:** If `swisseph` library is not found, it falls back to a very low-precision mock calculation engine. This is a critical accuracy risk.
    -   **Bloat:** The core engine is cluttered with non-Vedic systems (Maya, Bazi, I Ching, Human Design, etc.), which complicates the "Vedic First" redesign.
    -   **Birth Data:** Timezone handling uses `timezonefinder` with a fallback guess mechanism, which violates the "never guess" rule.

### B. Prediction Engine (`app/astrology/predictions/`)
-   **Rule-Based:** Most predictions are rule-based, using a `factor`-based scoring system.
-   **LLM-Generated:** The "AI Note" in `predictions` and the "AstroChat" use LLMs to interpret the calculated data.
-   **Missing Corroboration:** While it uses multiple factors, it lacks the formal "Corroboration Engine" requested (e.g., explicitly linking D1, Dasha, Transit, and D10 into a single corroborated conclusion).
-   **Strength Scaling:** Uses a 0-100 score and labels (Excellent, Good, etc.), but doesn't implement the requested "Prediction Strength" hierarchy (VERY STRONG, STRONG, etc.) with explicit evidence/conflict breakdown.

### C. Remedy Engine (`app/astrology/remedies/`)
-   **Current State:** Basic mapping of planets to mantras, charities, and lifestyle changes.
-   **Hard-coded Logic:** Remedies are mostly statically mapped based on planet debilitation or functional malefic status.
-   **Gemstones:** Casually recommended in `GEMSTONE_DATABASE`, which is explicitly forbidden in the redesign requirements.
-   **Missing:** No prioritization, no tracking, and no timing logic for remedies.

### D. AI Engine & Prompting
-   **Current State:** Direct integration with OpenAI/Ollama in `routes.py`.
-   **Prompts:** Simple system prompts for "Jyotishi" persona.
-   **Risks:** No safety filtering, no response validation (AI can invent facts), and no abstraction for switching between local (Ollama) and cloud (Gemini/OpenAI) providers.

### E. Data Models & Database
-   **Current State:** Uses `CanonicalChart` Pydantic model. Storage is a mix of `flask-sqlalchemy` (local) and `google-cloud-firestore` (cloud).
-   **Risks:** Models are bloated with non-Vedic data (Maya, Human Design). No models for Remedy Tracking or Prediction Outcome feedback.

## 3. Existing Calculation Accuracy Risks
1.  **Mock Fallback:** `swe_proxy.py` contains a mock engine that returns dummy positions if `swisseph` isn't installed. This is extremely dangerous for a professional astrology tool.
2.  **Timezone Guessing:** The `api/external.py` module guesses timezones based on longitude if the API fails, which can lead to significant errors in Lagna and Dasha.
3.  **Birth Time Confidence:** The system does not currently track or display birth-time confidence (High/Med/Low), which is critical for timing accuracy.

## 4. Existing Prediction Accuracy Risks
1.  **Single-Factor Bias:** Some prediction modules (like `personality.py` or basic `health.py`) rely heavily on single placements without enough corroboration from Varga charts or Dasha.
2.  **Timing Vagueness:** Predictions currently show a general "score" for the day/domain but don't define clear event windows (Start/Peak/End).
3.  **Conflict Handling:** The system currently averages scores rather than explicitly identifying and presenting conflicting astrological indications to the user.

## 5. Missing Capabilities
-   **Prediction Corroboration Engine:** Logic to strictly require multiple signals before making a major life prediction.
-   **Timing Window Engine:** Deterministic calculation of specific dates for career changes, marriage, etc.
-   **Remedy Prioritization & Tracking:** A system to tell the user which 3 remedies are most important TODAY and track their performance.
-   **Prediction Feedback Loop:** User-reported outcomes to validate the rule-based engine.
-   **Native Android App:** The project lacks a native mobile interface.

## 6. Free-Tier Dependencies & Tech Stack
-   **Calculation:** `pyswisseph` (Free, Local) - Excellent.
-   **AI:** Currently `openai` (Paid) or `ollama` (Free, Local). Need to move towards `Gemini` (Free Tier) or strictly `Ollama`.
-   **Geocoding:** `Nominatim` (Free), `OpenCage` (Free Tier).
-   **Database:** `SQLite` (Free, Local), `Firestore` (Free Tier).
-   **Hosting:** `Gunicorn/Flask` (Open Source).

## 7. Recommended Architecture Redesign

### Layered Architecture:
1.  **Vedic Core:** Cleaned-up `VedicEngine` focusing strictly on Parashari principles.
2.  **Evidence Engine:** A new module to synthesize D1, Varga, Dasha, and Transits into "Evidence Objects".
3.  **Timing Engine:** A specialized engine for calculating event windows (Start, Peak, End).
4.  **Remedy Engine:** Redesigned for prioritization and safety, integrated with a `RemedyTracker`.
5.  **AI Layer:** A provider-agnostic interface for explanations and natural language.
6.  **Android App:** Native Kotlin/Compose app consuming the Backend API or implementing local engine logic.

## 8. Migration Plan

1.  **Phase 1: Vedic Core Purification:** Remove non-Vedic bloat from `CanonicalChart` and `calculate_chart_data`.
2.  **Phase 2: Timing Engine:** Implement logic to calculate precise start/peak/end dates for dasha/transit intersections.
3.  **Phase 4: Evidence & Corroboration:** Refactor `predictions/engine.py` to use the multi-factor corroboration logic.
4.  **Phase 5: Remedy Engine Redesign:** Implement prioritization and safety filters.
5.  **Phase 6: Tracking & Feedback:** Add `PredictionTracker` and `RemedyTracker` database models and routes.
6.  **Phase 7: Android Foundation:** Set up the Android project structure (Kotlin/Compose/Retrofit).
7.  **Phase 8: UI/UX Redesign:** Implement the "Decision System" dashboard.

## 9. Files to Modify/Create

-   **Modify:**
    -   `app/astrology/core/chart.py` (Purification)
    -   `app/astrology/core/models.py` (Structure)
    -   `app/astrology/predictions/engine.py` (Corroboration)
    -   `app/astrology/remedies/engine.py` (Prioritization)
    -   `app/routes.py` (API endpoints for tracking)
-   **Create:**
    -   `app/astrology/evidence/` (Corroboration logic)
    -   `app/astrology/timing/precision.py` (Window logic)
    -   `app/astrology/ai/provider.py` (AI Abstraction)
    -   `app/astrology/tracking/` (Outcome & Remedy tracking)
    -   `android/` (New native Android module)

## 10. Protected Files
-   `ephe/` directory (Ephemeris data).
-   `tests/regression/golden_charts.json` (Critical for validation).
-   `app/astrology/core/swe_proxy.py` (Needs logic change but must be kept as the proxy).

## 11. Testing Plan
-   Unit tests for the new **Evidence Engine** (ensuring multi-factor requirement).
-   Unit tests for **Timing Windows**.
-   Integration tests for **AI Abstraction**.
-   Android UI tests for the new dashboard.
