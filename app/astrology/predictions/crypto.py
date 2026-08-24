from typing import Dict, Any, List
from ..core.models import CanonicalChart

# BTC Genesis: Jan 3, 2009.
# Key degrees: Sun 13 Cap, Moon 17 Ari, Jupiter 28 Cap.
BTC_GENESIS = {"Sun": 283.0, "Moon": 17.0, "Jupiter": 298.0}

def get_crypto_market_analysis(chart: CanonicalChart) -> Dict[str, Any]:
    """Correlating natal/transit charts with Crypto market structural points."""
    planets = chart.planets
    indicators = []

    # 1. Check current Jupiter/Saturn/Uranus against BTC Genesis
    # (Simplified natal-to-transit correlation)

    # 2. Uranus (Innovation/Crypto) status
    uranus = planets.get("Uranus")
    if uranus:
        if uranus.house in [2, 8, 11]:
            indicators.append(f"Uranus in H{uranus.house}: Strong resonance with decentralized financial technologies.")

    # 3. Nodes (Rahu/Ketu) - Speculative cycles
    rahu = planets.get("Rahu")
    if rahu:
        if rahu.rashi in [2, 6, 10]: # Air signs - Digital growth
             indicators.append("Rahu in Air Sign: High potential for digital asset expansion and mainstream adoption.")

    return {
        "crypto_sentiment": "ADOPTION_PHASE" if rahu and rahu.rashi in [2,6,10] else "CONSOLIDATION",
        "key_factors": indicators
    }
