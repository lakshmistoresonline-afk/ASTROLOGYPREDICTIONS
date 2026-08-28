# CORROBORATION ENGINE AUDIT

## 1. SIGNAL INDEPENDENCE
- **Problem**: Previously, "10th house" and "10th lord" were counted as independent.
- **Solution**: Implemented a **Weighted Synthesis** where linked factors share the same hierarchy level (Secondary) or are grouped into a single Primary driver (Dasha).

## 2. WEIGHTING MATRIX
| Signal Type | Weight | Role |
| :--- | :--- | :--- |
| **PRIMARY** | 1.0 | The "Trigger" (Dasha) |
| **SECONDARY** | 0.7 | The "Foundation" (Natal/Varga) |
| **SUPPORTING** | 0.3 | The "Nuance" (Yoga/Nakshatra) |
| **CONFLICT** | -0.5 | The "Friction" (Affliction) |

## 3. STRENGTH LOGIC
- **VERY STRONG**: Weighted Score >= 2.0 (e.g., 1 Primary + 1 Secondary + 1 Supporting).
- **STRONG**: Weighted Score >= 1.4 (e.g., 2 Secondary).
- **MODERATE**: Weighted Score >= 0.8.
- **MIXED**: Any weighted score > 1.0 that also contains CONFLICT signals.

## 4. TRANSPARENCY
The `DomainPrediction` model now explicitly separates `supporting_signals` from `conflicting_signals`, allowing the UI to show the "Why" behind the classification.

**Status**: **VERIFIED**
