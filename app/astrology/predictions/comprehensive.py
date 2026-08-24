from typing import Dict, List, Any
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

# Domain Mapping: (Primary House, Karaka Planet, Relevant Varga, Description, Focus)
DOMAIN_MAP = {
    "Personality & Soul": (1, "Sun", "D1", "Your core essence and physical constitution."),
    "Wealth & Gains": (11, "Jupiter", "D2", "Income streams and material desires."),
    "Assets & Family": (2, "Venus", "D2", "Accumulated wealth and family values."),
    "Property & Assets": (4, "Mars", "D4", "Ownership of land and home."),
    "Spirituality & Luck": (9, "Jupiter", "D20", "Faith and spiritual inclinations."),
}

def get_comprehensive_predictions(chart: CanonicalChart, transit_chart: dict = None, current_dasha: str = None) -> List[DomainPrediction]:
    results = []
    planets = chart.planets
    asc_rashi = chart.asc_rashi
    sav = chart.ashtakavarga.get("SAV", [28] * 12)

    for domain, (house_num, karaka, varga_key, desc) in DOMAIN_MAP.items():
        factors = []

        # 1. Lord Placement
        lord_name = chart.house_lords[house_num]
        lord = planets[lord_name]

        factors.append(EvidenceEngine.create_factor(
            "Lord Placement", "lord", "positive" if lord.house not in [6, 8, 12] else "negative", 10,
            f"Domain Lord {lord_name} in House {lord.house}: Defines the basic manifestation of this area."
        ))

        # 2. Dignity
        if "Exalted" in lord.dignity:
            factors.append(EvidenceEngine.create_factor("Lord Dignity", "lord", "positive", 15, "Lord is Exalted: Providing significant success potential."))
        elif "Debilitated" in lord.dignity:
            factors.append(EvidenceEngine.create_factor("Lord Dignity", "lord", "negative", 15, "Lord is Debilitated: May cause delays or challenges."))

        # 3. Ashtakavarga
        house_rashi = (asc_rashi + house_num - 1) % 12
        points = sav[house_rashi]
        if points >= 30:
            factors.append(EvidenceEngine.create_factor("SAV Points", "ashtakavarga", "positive", 12, f"High SAV points ({points}) provide strong energetic support."))
        elif points < 25:
            factors.append(EvidenceEngine.create_factor("SAV Points", "ashtakavarga", "negative", 8, f"Lower SAV points ({points}) indicate a need for more effort."))

        # 4. Transit Context
        if transit_chart:
            # Simple check
            t_planets = transit_chart.get("planets", {})
            if lord_name in t_planets:
                t_rashi = t_planets[lord_name]["rashi"]
                t_house = (t_rashi - asc_rashi + 12) % 12 + 1
                if t_house in [1, 4, 7, 10, 5, 9, 11]:
                    factors.append(EvidenceEngine.create_factor("Transit", "transit", "positive", 10, f"Lord {lord_name} is transiting a favorable house ({t_house})."))
                elif t_house in [6, 8, 12]:
                    factors.append(EvidenceEngine.create_factor("Transit", "transit", "negative", 10, f"Lord {lord_name} is transiting a challenging house ({t_house})."))

        results.append(analyze_domain(domain, factors, desc + " Strength: {score}%.", chart=chart))

    return results
