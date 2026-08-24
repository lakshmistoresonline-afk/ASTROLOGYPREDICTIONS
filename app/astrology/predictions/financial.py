from typing import Dict, Any, List
from ..core.models import CanonicalChart

def get_financial_market_indicators(chart: CanonicalChart) -> Dict[str, Any]:
    """
    Financial Astrology: Analyzing global market sentiment based on transits.
    Jupiter (Expansion), Saturn (Contraction), Rahu (Speculation).
    """
    planets = chart.planets

    indicators = []

    # 1. Jupiter-Saturn Cycle
    # Conjunction: New era (20 years)
    # Square/Opposition: Financial tension
    jup = planets.get("Jupiter")
    sat = planets.get("Saturn")
    if jup and sat:
        diff = abs(jup.longitude - sat.longitude) % 360
        if diff > 180: diff = 360 - diff

        if diff < 10:
            indicators.append("Jupiter-Saturn Conjunction: Major restructuring of global financial systems.")
        elif abs(diff - 90) < 10:
            indicators.append("Jupiter-Saturn Square: Market friction and regulatory challenges.")

    # 2. Rahu in Finance Houses (2, 5, 8, 11)
    rahu = planets.get("Rahu")
    if rahu and rahu.house in [2, 5, 8, 11]:
        indicators.append(f"Rahu in H{rahu.house}: High speculative volatility and unconventional wealth trends.")

    # 3. Mercury Retrograde (Trading Glitches)
    merc = planets.get("Mercury")
    if merc and merc.is_retrograde:
        indicators.append("Mercury Retrograde: Caution advised in contracts and high-frequency trading.")

    return {
        "market_sentiment": "BULLISH" if "Jupiter" in [p for p in planets if planets[p].house in [2, 11]] else "BEARISH",
        "key_indicators": indicators
    }
