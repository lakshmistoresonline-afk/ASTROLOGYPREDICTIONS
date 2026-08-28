# FINAL PREDICTION QUALITY GAP ANALYSIS

## 1. CURRENT IMPLEMENTATION SUMMARY
The system has transitioned to a deterministic core using an isolated Swiss Ephemeris service. It features a multi-factor corroboration framework and a prioritized remedy engine.

- **Calculation Core**: Dockerized FastAPI service with `pyswisseph`.
- **Framework**: Evidence-based synthesis requiring 3+ signals for strong predictions.
- **Timing**: Placeholder logic using Antardasha periods and current month defaults.
- **Remedies**: Severity-based ranking focusing on the top 3 affected planets.
- **Tracking**: Infrastructure for reporting outcomes and remedy streaks is present.

## 2. VALIDATED COMPONENTS
- [x] **Deterministic Dependency**: Hardened Swiss Ephemeris requirement (no mocks).
- [x] **Vedic Standard**: Whole Sign houses and Lahiri Ayanamsa enforced.
- [x] **Vimshottari Sequence**: Standard 120-year cycle with proportional sub-periods.
- [x] **Divisional Scope**: D1-D60 calculation logic implemented.

## 3. UNVALIDATED COMPONENTS & RISKS

### A. Calculation Risks
- **Reference Accuracy**: No automated validation suite currently compares longitudes against established software (e.g., Astro.com/Jagannatha Hora).
- **Node Precision**: Current use of `MEAN_NODE`. Standard professional preference often requires a choice or strictly `TRUE_NODE`.
- **Ayanamsa Verification**: Need to confirm the precise decimal accuracy of the Lahiri implementation at epoch boundaries.
- **Timezone Gaps**: Potential for 1-hour errors during historical DST changes or "Midnight Birth" edge cases (00:00 vs 23:59).

### B. Prediction Risks
- **Weighted Evidence**: Current `CorroborationEngine` uses simple signal counts. It does not distinguish between a "Primary" signal (Dasha) and a "Supporting" signal (Nakshatra).
- **Independence Audit**: Signals like "10th house activation" and "10th lord placement" are mathematically related and should not be counted as two independent corroborations.
- **Rule Consistency**: Domain-specific logic (Career vs. Marriage) is currently too generic; it lacks specialized classical rules for each category.

### C. Timing Risks
- **Dynamic Triggers**: The `TimingWindowEngine` is too static. It lacks logic to detect precise "Peak" moments like planetary ingresses, retrograde stations, or combustion start/end.
- **Boundary Handling**: Dasha changes exactly at 00:00 UTC vs Local Time requires strict validation.

### D. Remedy Risks
- **Nature of Remedy**: Current engine recommends strengthening debilitated planets without checking if they are functional malefics (which could increase friction).
- **Remedy Categories**: Missing the "Pacify vs. Strengthen vs. Balance" hierarchy.

## 4. TEST COVERAGE GAPS
- [ ] Comparison tests with known reference charts.
- [ ] Boundary tests for midnight and DST transitions.
- [ ] Stress tests for high-volume transit scanning.
- [ ] Validation of divisional chart placements for specialized domains.

## 5. RECOMMENDED FIXES

### Phase 1: Deterministic Validation
- Implement `EPHEMERIS_VALIDATION_REPORT.md` using 5 golden charts.
- Strictly audit `MEAN_NODE` vs `TRUE_NODE` and make it a configuration.

### Phase 2: Evidence Hierarchy
- Refactor `framework.py` to use a weighted hierarchy:
  - **PRIMARY (Weight 1.0)**: Mahadasha/Antardasha.
  - **SECONDARY (Weight 0.7)**: D1/Divisional Kendra/Trikona.
  - **SUPPORTING (Weight 0.3)**: Nakshatra, Secondary aspects.

### Phase 3: Specialized Domain Engines
- Create separate rule files for `CareerEngine`, `MarriageEngine`, etc., each defining its own "Independent Factors" and "Conflicting Indicators".

### Phase 4: Dynamic Timing
- Refactor `precision.py` to scan for planetary ingress into target houses to define the "Peak" window.

### Phase 5: Safe Remedy Logic
- Introduce functional benefic/malefic checks before recommending "Strengthen" (Mantra) vs "Pacify" (Charity).

---
**Lead Architect Signature:** [Awaiting approval to proceed with Implementation]
