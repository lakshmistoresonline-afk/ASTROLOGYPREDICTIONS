from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine, are_associated

def get_career_prediction(chart: CanonicalChart, domain_type: str = "Career & Authority", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Professional Grade Career Analysis: Houses (10, 6, 7), D10, SAV, and timing."""
    factors = []

    planets = chart.planets
    asc_rashi = chart.asc_rashi
    sav = chart.ashtakavarga.get("SAV", [28] * 12)
    house_lords = chart.house_lords

    # 1. THE 10th HOUSE
    tenth_lord_name = house_lords[10]
    tenth_lord = planets[tenth_lord_name]
    tenth_house_rashi = (asc_rashi + 9) % 12

    from .data import HOUSE_INTERPRETATIONS

    factors.append(EvidenceEngine.create_factor(
        "10th Lord Placement", "lord", "positive", 10,
        f"10th Lord {tenth_lord_name} in House {tenth_lord.house}: {HOUSE_INTERPRETATIONS.get(tenth_lord.house, '')}"
    ))

    # Dignity
    if "Exalted" in tenth_lord.dignity:
        factors.append(EvidenceEngine.create_factor("10th Lord Dignity", "lord", "positive", 25, "10th Lord is Exalted: Indication of high fame and peak status."))
    elif tenth_lord.dignity == "Own Sign":
        factors.append(EvidenceEngine.create_factor("10th Lord Dignity", "lord", "positive", 15, "10th Lord in own sign: Strong professional resilience."))
    elif "Debilitated" in tenth_lord.dignity:
        factors.append(EvidenceEngine.create_factor("10th Lord Dignity", "lord", "negative", 20, "10th Lord is Debilitated: Challenges with authority or effort results."))

    # 2. ASHTAKAVARGA
    av_points = sav[tenth_house_rashi]
    if av_points >= 30:
        factors.append(EvidenceEngine.create_factor("SAV Strength", "ashtakavarga", "positive", 10, f"High SAV ({av_points}) in 10th house: Strong energetic support for career goals."))
    elif av_points < 25:
        factors.append(EvidenceEngine.create_factor("SAV Strength", "ashtakavarga", "negative", 8, f"Low SAV ({av_points}) in 10th house: Work may feel draining or lack rewards."))

    # 3. D10 CONFIRMATION
    varga_confirmed = False
    d10 = chart.divisional_charts.get("D10", {})
    if d10:
        d10_lagna = d10.get("Lagna", 0)
        d10_pos = d10.get(tenth_lord_name)
        if d10_pos is not None:
            rel_h = (d10_pos - d10_lagna + 12) % 12 + 1
            if rel_h in [1, 4, 7, 10]:
                varga_confirmed = True
                factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, f"10th Lord is in a Kendra (H{rel_h}) in D10, confirming professional success."))

        # Advanced D10: 10th from D10 Lagna and Arudha Lagna (AL)
        # Check if AK or AmK is in 10th house of D10
        amk_name = chart.jaimini_karakas.get("Amatyakaraka (AmK) - Career/Mind")
        if amk_name:
            amk_d10 = d10.get(amk_name)
            if amk_d10 is not None:
                h_amk = (amk_d10 - d10_lagna + 12) % 12 + 1
                if h_amk in [1, 4, 7, 10, 5, 9]:
                     factors.append(EvidenceEngine.create_factor("Career Mastery", "varga", "positive", 15, f"Amatyakaraka {amk_name} is well-placed (H{h_amk}) in Dashamsha, indicating high skill and authority."))

    # 3b. Advanced Jaimini Career Insights
    # ... existing ...

    # 3c. Yoga Strength
    for y in chart.yogas:
        if "Mahapurusha" in y["name"]:
            # Check if yoga planet is linked to 10th house
            y_planet = y["name"].split(' ')[0] # (e.g., 'Hamsa' -> Jupiter)
            # Actually Mahapurusha names are Ruchaka (Mars), Bhadra (Merc), etc.
            names = {"Ruchaka": "Mars", "Bhadra": "Mercury", "Hamsa": "Jupiter", "Malavya": "Venus", "Shasha": "Saturn"}
            p_name = names.get(y["name"].split(' ')[0])
            if p_name:
                factors.append(EvidenceEngine.create_factor("Mahapurusha Impact", "yoga", "positive", 20, f"The presence of {y['name']} (ruled by {p_name}) provides exceptional strength and authority in your professional path."))
    # A. Amatyakaraka (AmK)
    amk_name = chart.jaimini_karakas.get("Amatyakaraka (AmK) - Career/Mind")
    if amk_name:
        amk = planets[amk_name]
        factors.append(EvidenceEngine.create_factor(
            "Amatyakaraka", "planet", "positive" if amk.house in [1, 4, 7, 10, 5, 9, 11] else "neutral", 15,
            f"{amk_name} is your Amatyakaraka (Career Indicator). Its position in House {amk.house} defines your primary professional drive."
        ))

    # B. Arudha 10th (A10)
    a10_rashi = chart.arudha_padas.get("A10")
    if a10_rashi is not None:
        from ..core.houses import RASHI_NAMES
        factors.append(EvidenceEngine.create_factor(
            "Arudha 10th", "yoga", "positive", 10,
            f"Arudha of the 10th house falls in {RASHI_NAMES[a10_rashi]}, indicating how your professional status is recognized by society."
        ))

    # C. Argala on 10th House
    argala_10 = chart.argala_analysis.get(10, {})
    primary_argala_houses = argala_10.get("primary", [])
    obstructing_houses = argala_10.get("obstructing", [])

    benefics = ["Jupiter", "Venus", "Mercury", "Moon"]
    argala_planets = [p for p, info in planets.items() if info.house in primary_argala_houses and p in benefics]
    if argala_planets:
        factors.append(EvidenceEngine.create_factor(
            "House Support", "house", "positive", 12,
            f"The 10th house has positive intervention (Argala) from {', '.join(argala_planets)}, facilitating career progress."
        ))

    # D. Varnada Lagna (V10) - Professional Identity
    v10_rashi = chart.varnada_lagna.get(10)
    if v10_rashi is not None:
        from ..core.houses import RASHI_NAMES
        factors.append(EvidenceEngine.create_factor(
            "Professional Status", "yoga", "positive", 15,
            f"Varnada Lagna for the 10th house falls in {RASHI_NAMES[v10_rashi]}, identifying your specific professional archetype."
        ))

    # 4. SERVICE vs. BUSINESS
    l6_name = house_lords[6]
    l7_name = house_lords[7]
    l6 = planets[l6_name]
    l7 = planets[l7_name]

    if tenth_lord.house == 6 or are_associated(tenth_lord_name, l6_name, planets):
        factors.append(EvidenceEngine.create_factor("Employment Bias", "lord", "positive", 8, "Strong connection to the 6th house favors regular employment and service-oriented roles."))
    if tenth_lord.house == 7 or are_associated(tenth_lord_name, l7_name, planets):
        factors.append(EvidenceEngine.create_factor("Independent Practice", "lord", "positive", 8, "Connection between 10th and 7th houses favors public dealings or independent consultancy."))

    # 5. GOVERNMENT vs. PRIVATE
    sun = planets["Sun"]
    saturn = planets["Saturn"]
    if sun.house in [1, 10, 11] or "Exalted" in sun.dignity:
        factors.append(EvidenceEngine.create_factor("Government Authority", "planet", "positive", 12, "Strong Sun placement favors roles in government, administration, or leadership."))
    if saturn.house in [10, 11]:
        factors.append(EvidenceEngine.create_factor("Steady Growth", "planet", "positive", 5, "Saturn in career sectors favors stability and persistence in corporate or technical fields."))

    # 6. SPECIALIZED ROLES
    # Technical (Mars) vs Creative (Venus)
    mars = planets["Mars"]
    venus = planets["Venus"]
    if "Exalted" in mars.dignity:
        factors.append(EvidenceEngine.create_factor("Execution Power", "planet", "positive", 8, "Strong Mars indicates executive ability and success in technical or competitive sectors."))
    if "Exalted" in venus.dignity:
        factors.append(EvidenceEngine.create_factor("Creative Path", "planet", "positive", 8, "Strong Venus favors professions in design, media, or diplomacy."))

    # 7. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        d_conf = timing_data.get("dasha_confirmed", False)
        if d_conf:
            factors.append(EvidenceEngine.create_factor("Career Activation", "dasha", "positive", 12, "The current Dasha period activates career-supporting planets, indicating professional growth."))
        if t_conf:
            factors.append(EvidenceEngine.create_factor("Immediate Opportunity", "transit", "positive", 8, "Current transits are exceptionally favorable for new ventures or promotions."))

    summary_template = "Your professional trajectory strength is {score}%. Confidence: {confidence}."

    return analyze_domain(
        "Career & Authority",
        factors,
        summary_template,
        varga_data={"confirmed": varga_confirmed},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
