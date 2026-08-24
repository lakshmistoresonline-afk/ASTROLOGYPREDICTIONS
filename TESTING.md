# Testing Documentation

ASTROLOGYPREDICTIONS uses automated regression tests to ensure calculation integrity and deterministic prediction logic.

## 🧪 Golden Chart Regression Suite
Located at `tests/regression/test_astrology_core.py`, this suite verifies calculations against a dataset of "Golden Charts" (birth details with known, verified planetary positions and varga placements).

### Key Verification Areas:
- **Planetary Positions**: Sign, degree, and house placement in D1.
- **Varga Integrity**: Positions in divisional charts (D2, D3, D9, D10, D30, D60).
- **Ayanamsa**: Precise Lahiri ayanamsa calculation.
- **Panchang**: Tithi, Nakshatra, and Yoga limb accuracy.

## 🏃 How to Run Tests
1. Ensure the development environment is set up.
2. Run the full suite using pytest:
   ```bash
   python -m pytest tests/regression/
   ```

## 📐 Algorithmic Unit Tests
Individual engines (Shadbala, Yogas, Timing) are tested for logic consistency:
- **Shadbala**: verified against manual Virupa calculations for standard cases.
- **Yoga Detector**: tested for edge cases in planetary associations and house counts.
- **Divisional charts**: D2, D30, and D60 are tested for specific Parashari cycle accuracy.
