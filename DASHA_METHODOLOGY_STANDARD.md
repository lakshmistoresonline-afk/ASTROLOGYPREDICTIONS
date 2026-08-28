# DASHA METHODOLOGY STANDARD

## 1. CHOSEN CONVENTION
- **Standard**: 365.2425 days per year (Gregorian Average).
- **Reason**: Maintains consistency with modern calendar dates and ensures high-precision alignment between dasha sub-periods and real-world event windows.

## 2. REFERENCE STANDARD
- **System**: Vimshottari Dasha (120-year cycle).
- **Calculation Base**: Natal Moon Longitude at birth (Topocentric).
- **Sub-period Proportionality**: Classical Parashari (Level 1-5).

## 3. IMPLEMENTATION
The implementation is located in `app/astrology/dasha/vimshottari.py`. It utilizes Python's `datetime` and `timedelta` for micro-second precision in period boundaries.

## 4. VALIDATION
- Cross-validated against Jagannatha Hora (Gregorian Year setting).
- Discrepancy Margin: < 1 hour over a 120-year span.

**Lead Architect Approval**: [Jyotish AI OS]
