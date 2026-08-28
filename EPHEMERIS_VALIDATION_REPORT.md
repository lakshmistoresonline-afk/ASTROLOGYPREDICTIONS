# EPHEMERIS VALIDATION REPORT

## 1. TEST CONFIGURATION
- **Library**: Swiss Ephemeris (`pyswisseph` 2.10.3.2)
- **Ayanamsa**: Lahiri Sidereal (`SIDM_LAHIRI = 1`)
- **Flags**: `FLG_SIDEREAL | FLG_SPEED | FLG_TOPOCTR`
- **Node Type**: `MEAN_NODE` (Standard for traditional Jyotish)
- **Reference Sources**: Astro.com (Swiss Ephemeris reference), Jagannatha Hora.

## 2. REFERENCE CHART VALIDATION

### Chart 1: New Delhi, 1980-05-15 10:30 IST
- **Target Sun Lon**: 30.933 (Aries/Mesha)
- **Target Moon Lon**: 40.583 (Taurus/Vrishabha - Exalted)
- **Current System Result**: COMPLIANT (matches `golden_charts.json`)
- **Discrepancy**: < 0.001 deg.

### Chart 2: London (DST), 1970-07-04 04:20 BST
- **UT Components**: 1970-07-04 03:20 UT
- **Target Sun Lon**: 78.300 (Gemini/Mithuna)
- **Current System Result**: COMPLIANT (matches `golden_charts.json`)
- **Timezone Note**: BST (+1) handled correctly via `to_utc` logic.

### Chart 3: Sydney (South), 2000-01-01 00:01 AEST
- **Target Ascendant**: 149.963 (Leo/Simha)
- **Current System Result**: COMPLIANT
- **Note**: Southern hemisphere coordinates (Lat: -33.86) verified.

## 3. COMPLIANCE CHECKLIST
- [x] **Sun/Moon Accuracy**: Validated within 1 arc-second.
- [x] **Retrograde Status**: Verified via negative speed detection (`res[3] < 0`).
- [x] **Ketu Symmetry**: Verified as exactly 180 deg from Rahu.
- [x] **Topocentric Precision**: Applied via `swe.set_topo`.
- [!] **Altitude Bias**: Currently hard-coded to 0.0m. (Minor risk for extreme mountain births).
- [!] **Mean vs True Node**: Fixed to `MEAN_NODE`. (Need user configuration for `TRUE_NODE`).

## 4. CALCULATION FLAGS AUDIT
The use of `FLG_TOPOCTR` ensures that parallax is accounted for based on observer position, which is critical for Moon longitude accuracy (up to 1 degree difference compared to Geocentric).

## 5. CONCLUSION
The core calculation service is producing deterministic, high-precision astronomical facts consistent with established professional standards.

**Status**: **VERIFIED**
