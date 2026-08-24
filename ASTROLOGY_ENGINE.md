# Astrology Engine Documentation

The engine is built on **Swiss Ephemeris** and follows the **Parashari** system of Vedic Astrology.

## 🛠️ Core Algorithms

### 1. Planetary Strength (Shadbala)
Implemented all 6 components to determine the functional power of a planet:
- **Sthana Bala**: Positional strength (Exaltation, Varga).
- **Dig Bala**: Directional strength (Planets in specific houses).
- **Kala Bala**: Temporal strength (Day/Night, Paksha).
- **Cheshta Bala**: Motional strength (Retrograde, Speed).
- **Naisargika Bala**: Natural strength (Sun is strongest, Saturn weakest).
- **Drik Bala**: Aspectual strength (Weighted benefics vs malefics).

### 2. Divisional Charts (Vargas)
The engine supports all 16 major Vargas used for deep analysis:
- **D9 (Navamsha)**: Marriage and general fruit of D1.
- **D10 (Dashamsha)**: Career and public status.
- **D24 (Chaturvimshamsha)**: Education and learning.
- **D27 (Saptavimshamsha)**: General strengths and weaknesses.
- **D30 (Trimshamsha)**: Risks, character flaws, and inner challenges.
- **D60 (Shashtiamsha)**: High-resolution soul-level karmic mapping.

### 3. Timing Engine
Combines three distinct layers for event timing:
- **Vimshottari Dasha**: Identifies the major planetary cycles governing life phases.
- **Transits**: Analyzes current planetary positions relative to the natal moon and lagna.
- **Ashtakavarga (SAV)**: Uses Sarvashtakavarga points as a multiplier for transit impact, representing the "energetic capacity" of houses.

### 4. Yoga Engine
A detector for 100+ standard planetary combinations:
- **Rajayogis**: Success and rise in status.
- **Dhana Yogas**: Wealth accumulation.
- **Daridra Yogas**: Financial challenges and introspection.
- **Nabhasa Yogas**: Lifelong structural themes.

## 📐 Precision Standards
- **Sidereal Zodiac**: Lahiri Ayanamsa (Default).
- **House System**: Whole Sign Houses (Default).
- **Precision**: Topocentric coordinates (accounting for altitude and geographic location).
