# Astro Predictions — Swiss Ephemeris Licensing & Compliance

## 1. Ephemeris Engine
Astro Predictions utilizes the Swiss Ephemeris (Sweph) library (`swe_proxy.py`, `ephemeris.py`, `chart.py`) for high-precision astronomical calculations (Sidereal zodiac, Lahiri ayanamsa, mean nodes, Placidus/Whole Sign houses, topocentric coordinate transformation).

## 2. Licensing Compliance
- The Swiss Ephemeris is governed by the GNU General Public License (GPL) or a proprietary commercial license depending on distribution terms.
- Commercial deployments of Astro Predictions utilizing Swiss Ephemeris binaries/source code must adhere to GPL obligations or maintain valid commercial licensing agreements as required by Astrodienst AG.
- Calculation semantics and ephemeris binaries remain strictly isolated in the protected V3.15 calculation core (`app/astrology/core/`), ensuring complete reproducibility and compliance separation from application/commercial layers.
