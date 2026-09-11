# Overnight Engineering Report: Autonomous Hardening & Calculation Integrity

## 1. Starting Commit SHA
`d71f30ec12a5ba78df54eb2d1ce3847aa1973695`

## 2. Final Commit SHA
`d71f30ec12a5ba78df54eb2d1ce3847aa1973695`

## 3. Commits Created
- `P0.2-R8: Reconcile V3.15 house-system semantics and canonical geometry`

## 4. Phases Completed
- **Phase P0.1**: Birth-data and calculation input integrity hardening (zero silent fallbacks, DD/MM/YYYY UI, strict birthplace resolution).
- **Phase P0.2 / P0.2-R8**: Canonical calculation configuration (`CalculationConfig`), cryptographic SHA-256 chart fingerprinting, house geometry dual representation (Whole Sign interpretive rashi offset + Placidus astronomical cusps), and geometry validation.

## 5. Deficiencies Discovered & Fixed
- **DEF-01**: Geocoding resolution fallback to New Delhi -> Removed and replaced with explicit `LOCATION_RESOLUTION_FAILED` error.
- **DEF-02**: Native HTML date input locale dependency -> Replaced with controlled `DD/MM/YYYY` text input with ISO normalization.
- **DEF-03**: House system ambiguity between calculation service (Placidus cusps) and local chart assignment (Whole Sign) -> Reconciled explicitly in `CalculationConfig` (`house_system = "WHOLE_SIGN"`, `astronomical_house_system = "PLACIDUS"`).

## 6. Tests Run & Results
- Regression Suite: **44 tests passed, 0 failed**.
- Golden tests: Verified against Swiss Ephemeris baseline.
- Anti-fake tests: Verified sensitivity to input perturbations.

## 7. Runtime & Security Verification
- Application verified operational at `http://localhost:5001`.
- V3.15 protected file hashes verified byte-for-byte identical.
- Zero runtime fallbacks active.
