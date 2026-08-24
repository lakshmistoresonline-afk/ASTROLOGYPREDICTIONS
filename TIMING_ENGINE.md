# Timing Engine Documentation

The ASTROLOGYPREDICTIONS platform uses a three-layer synthesis for highly localized timing predictions.

## 🕒 Three-Layer Synthesis

### 1. Birth Promise (Natal Potential)
Identifies the baseline potential for any area of life (e.g., Career, Wealth) based on house lordship, planetary strength (Shadbala), and divisional chart confirmation (Varga).

### 2. Dasha Activation (Planetary Cycles)
Uses the **Vimshottari Dasha** system to identify which planets are currently governing the native's timeline.
- **Mahadasha**: Major life phase themes.
- **Antardasha**: Sub-period focus.
- A life area is "activated" if its primary lords or karakas are dasha rulers.

### 3. Transit Support (Current Cosmic Sky)
Analyzes current planetary positions relative to the natal moon and house cusps.
- **Benefic Transit**: Jupiter, Venus, or Mercury transiting key houses.
- **Ashtakavarga (SAV) Multiplier**: Transit results are weighted by Sarvashtakavarga points. A house with high SAV points (30+) has a greater "energetic capacity" to manifest the transit's results.

## 📐 Event Probability Model
The engine calculates a "Timing Score" (0-1.0) for every prediction:
- **High (0.7+)**: Strong alignment between dasha and transit.
- **Moderate (0.4-0.7)**: Dasha support with neutral transits, or vice-versa.
- **Low (<0.4)**: Neither dasha nor transits supportive.
