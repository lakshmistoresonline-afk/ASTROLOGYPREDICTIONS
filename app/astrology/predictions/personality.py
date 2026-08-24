from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_personality_prediction(chart: CanonicalChart, domain_type: str = "Personality & Temperament", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Deep Identity Analysis: Lagna, Sun, Moon, and Atmakaraka."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords
    sav = chart.ashtakavarga.get("SAV", [28] * 12)
    asc_rashi = chart.asc_rashi

    # 1. Lagna and Lagna Lord
    lagna_lord_name = house_lords[1]
    lagna_lord = planets[lagna_lord_name]

    factors.append(EvidenceEngine.create_factor(
        "Lagna Lord Placement", "lord", "positive" if lagna_lord.house not in [6, 8, 12] else "negative", 15,
        f"Lagna Lord {lagna_lord_name} in House {lagna_lord.house}: Defines the physical strength and life direction."
    ))

    if "Exalted" in lagna_lord.dignity:
        factors.append(EvidenceEngine.create_factor("Lagna Lord Dignity", "lord", "positive", 20, "Lagna Lord is Exalted: Exceptional vitality and leadership potential."))
    elif "Debilitated" in lagna_lord.dignity:
        factors.append(EvidenceEngine.create_factor("Lagna Lord Dignity", "lord", "negative", 15, "Lagna Lord is Debilitated: May indicate low confidence or physical sensitivity."))

    # 2. Solar Essence (Sun)
    sun = planets["Sun"]
    if sun.house in [1, 9, 10]:
        factors.append(EvidenceEngine.create_factor("Solar Vitality", "planet", "positive", 10, f"Sun in House {sun.house}: Strong sense of self and soul-purpose."))
    elif sun.house in [6, 8, 12]:
        factors.append(EvidenceEngine.create_factor("Solar Obscuration", "planet", "negative", 8, f"Sun in House {sun.house}: Soul-path may involve significant trials or isolation."))

    # 3. Lunar Mind (Moon)
    moon = planets["Moon"]
    if moon.house in [1, 4, 5, 9]:
        factors.append(EvidenceEngine.create_factor("Lunar Harmony", "planet", "positive", 10, f"Moon in House {moon.house}: Emotional stability and intuitive clarity."))
    elif moon.house in [6, 8, 12]:
        factors.append(EvidenceEngine.create_factor("Lunar Turbulence", "planet", "negative", 10, f"Moon in House {moon.house}: Tendency towards emotional fluctuation or deep introspection."))

    # 4. Ashtakavarga
    lagna_rashi = asc_rashi
    points = sav[lagna_rashi]
    if points >= 30:
        factors.append(EvidenceEngine.create_factor("Lagna SAV", "ashtakavarga", "positive", 12, f"High SAV in Lagna ({points}): Strong foundational energy and physical resilience."))
    elif points < 25:
        factors.append(EvidenceEngine.create_factor("Lagna SAV", "ashtakavarga", "negative", 8, f"Low SAV in Lagna ({points}): May require more conscious effort to maintain energy levels."))

    # 5. Varga Confirmation (D1)
    varga_confirmed = True # Primary chart is always confirmed for personality

    # 6. Advanced Jaimini & Yogi Insights
    # A. Arudha Lagna (AL) - Public Image
    al_rashi = chart.arudha_padas.get("AL")
    if al_rashi is not None:
        from ..core.houses import RASHI_NAMES
        factors.append(EvidenceEngine.create_factor(
            "Arudha Lagna", "yoga", "positive", 10,
            f"Arudha Lagna in {RASHI_NAMES[al_rashi]}: Defines how the world perceives you and your social status."
        ))

    # B. Yogi Planet - Luck
    yogi = chart.yogi_details.get("Yogi")
    if yogi == lagna_lord_name or yogi == "Sun":
        factors.append(EvidenceEngine.create_factor(
            "Yogi Protection", "planet", "positive", 15,
            f"The Yogi planet ({yogi}) is strongly linked to your identity, providing divine protection and luck."
        ))

    # C. Dagtha Rashi Check
    if asc_rashi in chart.dagtha_rashis:
        factors.append(EvidenceEngine.create_factor(
            "Dagtha Lagna", "house", "negative", 12,
            "Your Ascendant falls in a 'burnt' sign (Dagtha Rashi), indicating that personal efforts may face hidden hurdles or lack fulfillment."
        ))

    # D. Gandanta birth
    for g in chart.gandanta_alerts:
        if g["target"] == "Ascendant":
            factors.append(EvidenceEngine.create_factor(
                "Gandanta Birth", "house", "negative", 15,
                "Lagna Gandanta: Born during a major elemental junction, indicating high intensity and significant karmic lessons."
            ))

    # 7. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("dasha_confirmed"):
            factors.append(EvidenceEngine.create_factor("Dasha Activation", "dasha", "positive", 10, "The current dasha period activates primary personality planets, bringing self-realization."))

    summary_template = domain_type + " score: {score}%. Confidence: {confidence}."

    return analyze_domain(
        domain_type,
        factors,
        summary_template,
        varga_data={"confirmed": varga_confirmed},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
