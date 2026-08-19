# 🔮 Jyotish Dashboard: Forensic Audit Report

**Date:** 2026-08-18  
**Auditor:** Senior Jyotish Software Engineer / Python Architect  
**Project:** [Jyotish Dashboard](https://github.com/Aerofarmer/jyotish-dashboard.git)

---

## 🏗️ Architecture Assessment
The current architecture is a monolithic Flask application. While functional, the astrology logic is tightly coupled with the routing and template layers. The "Engine" is scattered across several modules in `app/astrology/`, making it difficult to test or upgrade individual calculation components without affecting the entire system.

*   **Status:** Needs Modularization (Phase 2).
*   **Risk:** High maintenance overhead; hard to implement complex multi-factor predictions.

## 📐 Calculation Assessment
The project uses **Swiss Ephemeris** (`pyswisseph`) for core astronomical data, which is excellent. However, several higher-level Vedic logic layers are implemented with simplistic approximations.

*   **Bugs:**
    *   **Boundary Errors:** Longitude handled with `% 360`, but house/nakshatra transitions lack high-precision verification (Phase 5).
    *   **Ketu Logic:** Hardcoded as `Rahu + 180`. While standard for Mean Node, it lacks support for True Node or specific ayanamsa-based corrections.
*   **Severity:** MEDIUM.

## 🧿 Prediction Assessment
The prediction engine in `predictions.py` is the weakest link. It uses a "Planet in House" lookup table with hardcoded strings and a simplistic `score += 1` / `score -= 1` logic.

*   **Bugs:**
    *   No functional benefic/malefic status used.
    *   No consideration of Shadbala or planetary strength.
    *   No Graha Drishti (Classical Vedic Aspects); only 0°/180° conjunctions are used.
*   **Severity:** CRITICAL (Primary Priority).

## 📅 Panchang Assessment
Panchang calculations are currently "approximate."

*   **Bugs:**
    *   **Tithi/Nakshatra Duration:** Calculated using average Moon speed (`0.549°/hour`). This leads to significant errors in Muhurta timings.
    *   **Rahu Kaal Mapping:** (Already identified and fixed by me in a previous turn, but logic remains simplistic).
*   **Severity:** HIGH.

## 🕰️ Dasha Assessment
Vimshottari Dasha implementation is basic.

*   **Bugs:**
    *   **Year Length:** Uses a fixed `365.25` day year. Vedic traditions often use `360` days or more precise solar years.
    *   **Boundary Timing:** The use of `timedelta` on fractional years can lead to drift in Pratyantardasha dates.
*   **Severity:** MEDIUM.

## 📊 Divisional Chart Assessment
Only **D1 (Rashi)** and **D9 (Navamsa)** are implemented.

*   **Bugs:**
    *   Navamsa is treated purely as a visual chart; it is not integrated into planetary strength or prediction scoring.
    *   No D10, D7, D24, etc., which are essential for domain-specific predictions (Career, Children, Education).
*   **Severity:** HIGH.

## 🔐 Security Assessment
*   **Vulnerabilities:**
    1.  **Flask Secret:** Weak hardcoded fallback in `app/__init__.py`.
    2.  **CORS:** Default `CORS(app)` allows all origins.
    3.  **IP Location:** `get_ip_location` uses non-SSL `http://ip-api.com`.
    4.  **Error Exposure:** Flask debug mode may be accidentally left on in some environments.
*   **Severity:** MEDIUM.

## 🗄️ Database Assessment
The project leverages a local JSON file (`data/charts.json`).

*   **Bugs:**
    *   **Persistence:** `docker-compose.yml` does not map a volume for the `data/` directory. All saved charts are lost when the container is recreated.
    *   **Concurrency:** No file locking. Concurrent writes to the JSON file will lead to data corruption.
*   **Severity:** CRITICAL.

## 🧪 Testing Assessment
The project has **ZERO** automated tests.

*   **Severity:** CRITICAL.

---

## 📋 Exact Bugs Discovered

| Bug ID | Component | Description | Affected File | Severity | Recommended Fix |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **B01** | Database | Data lost on Docker restart (No volume for `data/`). | `docker-compose.yml` | **CRITICAL** | Add volume mapping for `/app/data`. |
| **B02** | Panchang | Tithi/Nakshatra duration uses average speed. | `panchang.py` | **HIGH** | Use iterative root-finding with Swiss Ephemeris. |
| **B03** | Predictions | Chandra Bala uses Nakshatra index instead of Rashi. | `panchang.py` | **HIGH** | Pass Rashi index to `_calc_chandra_bala`. |
| **B04** | Predictions | Simplistic scoring (`+= 1`) ignores dignity/strength. | `predictions.py` | **CRITICAL** | Implement weighted scoring engine (Phase 18). |
| **B05** | Security | Hardcoded Flask secret fallback. | `__init__.py` | **MEDIUM** | Enforce environment variable check; fail otherwise. |
| **B06** | Astro | Ketu is a simple `+180` offset from Rahu. | `calculator.py` | **LOW** | Use `swe.calc_ut` with appropriate node flags. |

---

## 🛠️ Regression Test Requirements
*   Verification of planetary longitudes against NASA Horizons/JPL data.
*   Panchang limb transition time validation (Tithi/Nakshatra end times).
*   Dasha date boundary checks across 120-year cycles.
*   Multi-user write test for chart persistence.
