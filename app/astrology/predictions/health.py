from typing import Dict, Any
from ..strength.functional import RASHI_LORDS

def get_health_prediction(chart: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze health using 1st house (Ascendant), its lord, and Dusthana houses."""
    evidence = []
    score = 60.0 # Higher base for health

    planets = chart["planets"]
    asc_rashi = chart["asc_rashi"]

    # 1st house lord (Self/Vitality)
    asc_lord_name = RASHI_LORDS[asc_rashi]
    asc_lord = planets[asc_lord_name]

    # Sun/Moon (Vitality indicators)
    sun = planets["Sun"]
    moon = planets["Moon"]

    # 1. Analyze Ascendant Lord
    if "Exalted" in asc_lord["dignity"] or asc_lord["dignity"] == "Own Sign":
        evidence.append(f"✓ Ascendant lord ({asc_lord_name}) is strong (+15)")
        score += 15
    elif "Debilitated" in asc_lord["dignity"]:
        evidence.append(f"⚠ Ascendant lord ({asc_lord_name}) is Debilitated (-20)")
        score -= 20

    # 2. Analyze Sun (Karaka for health/vitality)
    if "Exalted" in sun["dignity"] or sun["dignity"] == "Own Sign":
        evidence.append("✓ Sun (Vitality) is strong (+10)")
        score += 10
    elif "Debilitated" in sun["dignity"]:
        evidence.append("⚠ Sun (Vitality) is weak (-10)")
        score -= 10

    # 3. Dusthana check (6, 8, 12)
    # Are many planets in Dusthana?
    dusthana_count = sum(1 for p, d in planets.items() if d["house"] in [6, 8, 12])
    if dusthana_count >= 4:
        evidence.append(f"⚠ Multiple planets ({dusthana_count}) in Dusthana houses (-15)")
        score -= 15

    # 4. Benefics in Kendra
    kendra_benefics = sum(1 for p, d in planets.items() if d["house"] in [1, 4, 7, 10] and p in ["Jupiter", "Venus"])
    if kendra_benefics >= 1:
        evidence.append("✓ Protective benefics in Kendra houses (+10)")
        score += 10

    score = max(0.0, min(100.0, score))

    return {
        "domain": "Health",
        "score": score,
        "evidence": evidence,
        "confidence": "HIGH" if len(evidence) >= 3 else "MEDIUM",
        "disclaimer": "This is a traditional astrological interpretation and is not medical advice or a diagnosis."
    }
