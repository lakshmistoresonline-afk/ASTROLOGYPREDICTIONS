from typing import Dict, Any
from ..strength.functional import RASHI_LORDS

def get_marriage_prediction(chart: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze marriage/relationships using 7th house, its lord, and Venus/Jupiter."""
    evidence = []
    score = 50.0

    planets = chart["planets"]
    asc_rashi = chart["asc_rashi"]

    # 7th house from Ascendant
    seventh_house_rashi = (asc_rashi + 6) % 12
    seventh_lord_name = RASHI_LORDS[seventh_house_rashi]
    seventh_lord = planets[seventh_lord_name]

    # significator
    venus = planets["Venus"]
    jupiter = planets["Jupiter"]

    # 1. Analyze 7th lord
    if "Exalted" in seventh_lord["dignity"]:
        evidence.append(f"✓ 7th lord ({seventh_lord_name}) is Exalted (+20)")
        score += 20
    elif seventh_lord["dignity"] == "Own Sign":
        evidence.append(f"✓ 7th lord ({seventh_lord_name}) is in its Own Sign (+15)")
        score += 15
    elif "Debilitated" in seventh_lord["dignity"]:
        evidence.append(f"⚠ 7th lord ({seventh_lord_name}) is Debilitated (-20)")
        score -= 20

    # 2. Analyze Venus (Karaka for marriage)
    if "Exalted" in venus["dignity"] or venus["dignity"] == "Own Sign":
        evidence.append("✓ Venus (Significator of Love) is strong (+15)")
        score += 15
    elif "Debilitated" in venus["dignity"]:
        evidence.append("⚠ Venus (Significator of Love) is weak (-15)")
        score -= 15

    # 3. 7th house occupants
    occupants = [p for p, data in planets.items() if data["house"] == 7]
    for p in occupants:
        p_data = planets[p]
        if p_data["functional_status"] == "Functional Benefic":
            evidence.append(f"✓ Benefic planet {p} in 7th house (+10)")
            score += 10
        elif p_data["functional_status"] == "Functional Malefic":
            evidence.append(f"⚠ Malefic planet {p} in 7th house (-10)")
            score -= 10

    # 4. Navamsa (D9) check
    d9 = chart["divisional"]["D9"]
    d9_lagna = d9["Lagna"]
    d9_seventh_rashi = (d9_lagna + 6) % 12
    if d9[seventh_lord_name] == d9_seventh_rashi:
        evidence.append("✓ 7th lord confirmed in 7th house in D9 (+15)")
        score += 15

    score = max(0.0, min(100.0, score))

    return {
        "domain": "Marriage & Relationships",
        "score": score,
        "evidence": evidence,
        "confidence": "HIGH" if len(evidence) >= 3 else "MEDIUM"
    }
