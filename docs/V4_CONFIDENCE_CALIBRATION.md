# V4 Confidence Calibration

## Calibration Model
V4 separates internal signal scoring from empirical prediction probability.
- **Raw Signal Score**: Internal deterministic confluence score (0–100).
- **Evidence Score**: Sum of weighted independent evidence items.
- **Contradiction Score**: Sum of conflicting indicators.
- **Birth-Time Stability**: Sensitivity factor derived from $\pm 15$ min Ascendant variation.

Until historical outcome tracking yields sufficient empirical verification data, confidence is marked as **INTERNAL / UNCALIBRATED** to prevent false precision.
