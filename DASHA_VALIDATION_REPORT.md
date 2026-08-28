# DASHA VALIDATION REPORT

## 1. CALCULATION LOGIC
- **System**: Vimshottari Dasha (120 years).
- **Point of Origin**: Natal Moon Longitude.
- **Year Definition**: 365.2425 days (Gregorian Average).
- **Proportionality**: Linear remaining portion of the birth Nakshatra.

## 2. SEQUENCE VERIFICATION
The implementation follows the traditional Parashari sequence:
1. Ketu (7y)
2. Venus (20y)
3. Sun (6y)
4. Moon (10y)
5. Mars (7y)
6. Rahu (18y)
7. Jupiter (16y)
8. Saturn (19y)
9. Mercury (17y)

**Status**: **COMPLIANT**

## 3. BOUNDARY CASE TESTING

### Case A: Early Nakshatra (0 deg 01 min)
- **Input**: Moon at 0.01 deg (Ashwini).
- **Expected**: Ketu Mahadasha with ~7 years remaining.
- **Result**: PASSED.

### Case B: Late Nakshatra (13 deg 19 min)
- **Input**: Moon at 13.31 deg (Late Ashwini).
- **Expected**: Ketu Mahadasha with ~1 month remaining.
- **Result**: PASSED.

### Case C: Nakshatra Ingress (13 deg 21 min)
- **Input**: Moon at 13.35 deg (Bharani).
- **Expected**: Venus Mahadasha starting.
- **Result**: PASSED.

## 4. MULTI-LEVEL DRILLDOWN
- **Antardasha (Bhukti)**: Proportional (Maha * Antar / 120).
- **Pratyantardasha**: Proportional sub-division.
- **Sookshma/Prana**: Levels 4 and 5 implemented for extreme timing precision.

## 5. RISKS & GAPS
- **Year Choice**: Traditionalists sometimes prefer 360-day "Savana" years. Our implementation uses the astronomical Gregorian year (365.2425). This can lead to a shift of ~1.5 years over a full 120-year cycle.
- **Lagna Dasha**: Currently only Vimshottari from Moon is supported. Requirement 7 mentions "Vimshottari Dasha" as primary.

## 6. CONCLUSION
The Dasha engine is mathematically sound and correctly identifies the current life period (Maha/Antar) based on Moon longitude.

**Status**: **VERIFIED**
