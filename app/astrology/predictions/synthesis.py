from typing import Dict, List, Any
from ..core.models import CanonicalChart, DomainPrediction

def synthesize_all_systems(chart: CanonicalChart, domain_name: str) -> List[str]:
    """
    Synthesize all implemented world-systems for a single domain.
    (Vedic, Western, Hellenistic, Chinese, etc.)
    """
    insights = []

    # 1. Vedic (Yogas)
    for y in chart.yogas:
        if domain_name.lower() in y["interpretation"].lower():
             insights.append(f"Vedic Yoga: {y['name']} - {y['interpretation']}")

    # 2. Western (Harmonics)
    for res in chart.harmonic_resonances:
        insights.append(f"Western Harmonic: {res}")

    # 3. Chinese (Bazi)
    if domain_name == "Personality":
        insights.append(f"Chinese Bazi: Day Master {chart.bazi_pillars.get('DayMaster')} ({chart.bazi_pillars.get('Element')})")

    # 4. Hellenistic (ZR)
    if domain_name in ["Career", "Success"]:
        insights.append("Hellenistic: Check Zodiacal Releasing peak periods for high-intensity manifestation windows.")

    # 5. Uranian
    if domain_name in ["Marriage", "Money", "Fame"]:
        pt = chart.uranian_formulas.get(domain_name)
        if pt is not None:
             insights.append(f"Uranian Point: Sensitive {domain_name} point calculated at {round(pt, 2)}°.")

    return insights
