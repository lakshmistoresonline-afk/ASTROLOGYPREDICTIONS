from typing import Dict, List, Any
from ..core.models import CanonicalChart, DomainPrediction, PredictionFactor
from ..core.houses import RASHI_LORDS
from ..strength.aspects import get_graha_drishti

# Domain Mapping: (Primary House, Karaka Planet, Relevant Varga, Description)
DOMAIN_MAP = {
    "Personality & Self": (1, "Sun", "D1", "Overall temperament, physical constitution, and self-expression."),
    "Early Education": (2, "Mercury", "D24", "Foundational learning and intellectual development in early years."),
    "Higher Education": (5, "Jupiter", "D24", "Intelligence, academic pursuits, and creative knowledge."),
    "Career & Profession": (10, "Saturn", "D10", "Professional success, authority, and public reputation."),
    "Business & Trade": (7, "Mercury", "D10", "Partnerships, commercial success, and independent ventures."),
    "Finance & Earnings": (11, "Jupiter", "D2", "Income streams, gains, and fulfillment of material desires."),
    "Wealth & Assets": (2, "Venus", "D2", "Accumulated wealth, family inheritance, and fixed assets."),
    "Marriage": (7, "Venus", "D9", "Quality of marital life and long-term legal partnerships."),
    "Relationships": (7, "Moon", "D9", "Interpersonal connections, social harmony, and love."),
    "Children": (5, "Jupiter", "D7", "Progeny, happiness from children, and future legacy."),
    "Family Happiness": (2, "Moon", "D1", "Domestic harmony and ties with extended family."),
    "Parents (Mother)": (4, "Moon", "D12", "Relationship with mother, domestic peace, and emotional support."),
    "Parents (Father)": (9, "Sun", "D12", "Relationship with father, guidance, and ancestral blessings."),
    "Siblings": (3, "Mars", "D3", "Support from siblings, courage, and communication."),
    "Health & Immunity": (1, "Sun", "D1", "Vitality and overall physical well-being."),
    "Health Challenges": (6, "Saturn", "D1", "Potential for ailments and recovery strength."),
    "Property & Real Estate": (4, "Mars", "D4", "Ownership of land, home, and stability in dwelling."),
    "Vehicles": (4, "Venus", "D4", "Comfort through transportation and luxury assets."),
    "Short Travel": (3, "Mercury", "D1", "Frequent journeys and short-distance movements."),
    "Long Travel & Pilgrimage": (9, "Jupiter", "D9", "Spiritual journeys and long-distance travel."),
    "Foreign Travel": (12, "Rahu", "D1", "International journeys and experiences in foreign lands."),
    "Foreign Employment": (10, "Saturn", "D10", "Working in foreign companies or overseas locations."),
    "Foreign Settlement": (12, "Saturn", "D4", "Long-term relocation to foreign countries."),
    "Legal & Disputes": (6, "Mars", "D1", "Handling of conflicts, litigation, and victory over rivals."),
    "Spirituality": (9, "Jupiter", "D20", "Spiritual depth, faith, and religious inclinations."),
    "Fame & Recognition": (10, "Sun", "D10", "Public visibility, awards, and widespread respect."),
    "Social Status": (10, "Jupiter", "D10", "Position in society and professional hierarchy."),
    "Government & Authority": (10, "Sun", "D10", "Interactions with state authorities and leadership roles."),
    "Leadership": (1, "Sun", "D1", "Ability to lead, command, and influence others."),
    "Life Purpose (Dharma)": (9, "Jupiter", "D1", "The core path and spiritual duty in this incarnation."),
    "General Life Themes": (1, "Moon", "D1", "The recurring patterns and overall quality of life."),
    "Longevity": (8, "Saturn", "D1", "Life force and endurance indicators.")
}

def get_comprehensive_predictions(chart: CanonicalChart, transit_chart: dict = None, active_yogas: List[Dict] = None, current_dasha: str = None) -> List[DomainPrediction]:
    results = []
    planets = chart.planets
    asc_rashi = chart.asc_rashi
    sav = chart.ashtakavarga.get("SAV", [28] * 12)

    # 1. Pre-calculate aspects on each house sign
    house_aspects = {h: [] for h in range(1, 13)}
    for p_name, p_data in planets.items():
        if p_name in ["Rahu", "Ketu"]: continue
        drishtis = get_graha_drishti(p_name, p_data.rashi)
        for target_rashi in drishtis:
            target_house = (target_rashi - asc_rashi + 12) % 12 + 1
            house_aspects[target_house].append(p_name)

    # 2. Extract Transit Context
    transit_map = {}
    if transit_chart:
        n_lagna = chart.asc_rashi
        for p, data in transit_chart["planets"].items():
            t_rashi = data["rashi"]
            t_house = (t_rashi - n_lagna + 12) % 12 + 1
            transit_map[p] = t_house

    for domain, (house_num, karaka, varga_key, desc) in DOMAIN_MAP.items():
        evidence = []
        score = 50.0

        # --- A. NATAL FOUNDATION (50% Weight) ---
        lord_name = chart.house_lords[house_num]
        lord = planets[lord_name]

        # House Lord Status
        if "Exalted" in lord.dignity: score += 15; evidence.append(f"✓ {domain} Lord is Exalted in Natal Chart (+15)")
        elif "Own Sign" in lord.dignity: score += 10; evidence.append(f"✓ {domain} Lord is in its Own Sign (+10)")
        elif "Debilitated" in lord.dignity: score -= 15; evidence.append(f"⚠ {domain} Lord is Debilitated in Natal Chart (-15)")

        # Ashtakavarga (SAV) Strength of the House
        house_rashi = (asc_rashi + house_num - 1) % 12
        points = sav[house_rashi]
        if points >= 30: score += 10; evidence.append(f"✓ High SAV score ({points}) makes this house a natural Power Zone (+10)")
        elif points < 25: score -= 8; evidence.append(f"⚠ Low SAV score ({points}) indicates low natural support for this domain (-8)")

        # Significator (Karaka)
        k_planet = planets.get(karaka)
        if k_planet and ("Exalted" in k_planet.dignity or "Own Sign" in k_planet.dignity):
            score += 8; evidence.append(f"✓ Natural Significator ({karaka}) is strong in birth chart (+8)")

        # --- B. DIVISIONAL DEPTH (Varga) ---
        varga_data = chart.divisional_charts.get(varga_key, {})
        if varga_data:
            l_v_rashi = varga_data.get(lord_name)
            v_lagna = varga_data.get("Lagna")
            if l_v_rashi is not None and v_lagna is not None:
                rel_h = (l_v_rashi - v_lagna + 12) % 12 + 1
                if rel_h in [1, 4, 7, 10, 5, 9]:
                    score += 10; evidence.append(f"✓ Varga Success: Lord is in House {rel_h} of {varga_key} (+10)")

        # --- C. DYNAMIC TIMING (Dasha & Transit) ---
        if current_dasha == lord_name or current_dasha == karaka:
            score += 15; evidence.append(f"⏳ TIMING: Current Dasha lord activates this domain (+15)")

        if transit_map:
            t_house = transit_map.get(lord_name)
            if t_house in [1, 4, 7, 10, 5, 9, 11]:
                score += 12; evidence.append(f"🚀 TRANSIT: {lord_name} is currently in a favorable house from Lagna (+12)")
            elif t_house in [6, 8, 12]:
                score -= 10; evidence.append(f"🌪 TRANSIT: {lord_name} is currently transiting a difficult house (-10)")

        score = max(0.0, min(100.0, score))

        results.append(DomainPrediction(
            domain=domain,
            score=round(score, 1),
            confidence="HIGH" if len(evidence) >= 5 else "MEDIUM",
            summary=desc,
            evidence=evidence,
            positive_factors=[],
            negative_factors=[],
            recommendations=[f"Maximize the results through consistent action during this period."]
        ))

    return results
