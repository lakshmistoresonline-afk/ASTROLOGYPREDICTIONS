# ASTRO PREDICTIONS V4 EXTERNAL ENGINE RESEARCH

## 1. Benchmark References
- **PyJHora**: Python implementation of classical Vedic astrology calculations (JHora standards). Used as a primary reference for Varga divisional chart mathematical validation.
- **VedAstro**: Open-source Vedic astrology engine and API providing extensive domain rules and benchmark datasets.
- **KOSMA**: Evidence synthesis and confirmation gate reference model.
- **AlmaMesh**: Astronomical reference architecture and license-clean ephemeris exploration.

## 2. Integration Policy
- External reference implementations are studied for algorithmic alignment and mathematical verification.
- Core astronomical calculations remain anchored to Swiss Ephemeris (`pyswisseph`) via the isolated FastAPI calculation service with seamless in-process fallback.
