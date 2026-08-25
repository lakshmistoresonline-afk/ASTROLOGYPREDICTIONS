from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine, are_associated

def get_marriage_prediction(chart: CanonicalChart, domain_type: str = "Marriage & Relationships", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Relationship Analysis: 7th House, Venus, and D9 (Navamsha)."""
    factors = []

    planets = chart.planets
    asc_rashi = chart.asc_rashi
    house_lords = chart.house_lords

    # 1. 7th HOUSE (PARTNERSHIPS)
    seventh_lord_name = house_lords[7]
    seventh_lord = planets[seventh_lord_name]

    factors.append(EvidenceEngine.create_factor(
        "7th Lord Placement", "lord", "positive" if seventh_lord.house not in [6, 8, 12] else "negative", 10,
        f"7th Lord {seventh_lord_name} in House {seventh_lord.house}: Defines your approach to partnership."
    ))

    # 2. VENUS (KARAKA FOR LOVE)
    venus = planets["Venus"]
    if "Exalted" in venus.dignity:
        factors.append(EvidenceEngine.create_factor("Venus Dignity", "planet", "positive", 20, "Venus is Exalted: Strong potential for a harmonious and supportive relationship."))
    elif "Debilitated" in venus.dignity:
        factors.append(EvidenceEngine.create_factor("Venus Dignity", "planet", "negative", 15, "Venus is Debilitated: May face delays or high expectations in relationships."))

    # 3. LOVE vs. ARRANGED
    fifth_lord_name = house_lords[5]
    if seventh_lord.rashi == planets[fifth_lord_name].rashi or are_associated(seventh_lord_name, fifth_lord_name, planets):
        factors.append(EvidenceEngine.create_factor("Relationship Nature", "yoga", "positive", 10, "Connection between 5th and 7th lords suggests a marriage based on love or deep personal choice."))

    # 4. STABILITY (JUPITER)
    jupiter = planets["Jupiter"]
    from ..strength.aspects import get_graha_drishti
    j_aspects = get_graha_drishti("Jupiter", jupiter.rashi or 0)

    seventh_lord_rashi = seventh_lord.rashi or 0
    if seventh_lord_rashi in j_aspects or 7 in [(r - asc_rashi + 12) % 12 + 1 for r in j_aspects]:
        factors.append(EvidenceEngine.create_factor("Marital Stability", "planet", "positive", 12, "Jupiter's benefic gaze on the 7th house/lord ensures wisdom and stability in the bond."))

    # 5. SEPARATION INDICATORS
    malefics = ["Mars", "Saturn", "Rahu", "Ketu"]
    affliction_count = sum(1 for p in malefics if planets[p].house == 7)
    if affliction_count >= 2:
        factors.append(EvidenceEngine.create_factor("Separation Risk", "planet", "negative", 20, "Presence of multiple challenging planets in the 7th house may cause significant turbulence or separation."))
    elif seventh_lord.house in [6, 8, 12]:
        factors.append(EvidenceEngine.create_factor("Relationship Challenges", "lord", "negative", 15, "7th Lord in a difficult house suggests karmic tests or delays in marital fulfillment."))

    # 6. D9 CONFIRMATION
    varga_confirmed = False
    d9 = chart.divisional_charts.get("D9", {})
    if d9:
        d9_lagna = d9.get("Lagna", 0)
        d9_pos = d9.get(seventh_lord_name)

        # Check if D1 Lagna lord is Vargottama or in good D9 house
        l1_name = house_lords[1]
        if planets[l1_name].is_vargottama:
            factors.append(EvidenceEngine.create_factor("Vargottama Lagna Lord", "varga", "positive", 10, "Stability of the self (Lagna Lord) in Navamsha supports long-term commitment."))

        if d9_pos is not None:
            rel_h = (d9_pos - d9_lagna + 12) % 12 + 1
            if rel_h in [1, 4, 7, 10, 5, 9]:
                varga_confirmed = True
                factors.append(EvidenceEngine.create_factor("Navamsha Support", "varga", "positive", 15, f"7th lord is well-placed (H{rel_h}) in Navamsha, confirming the fruit of the relationship."))

    # 6b. Advanced Jaimini Marriage Insights
    # A. Upapada Lagna (UL) - A12
    ul_rashi = chart.arudha_padas.get("A12")
    if ul_rashi is not None:
        from ..core.houses import RASHI_NAMES
        factors.append(EvidenceEngine.create_factor(
            "Upapada Lagna", "yoga", "positive", 10,
            f"Upapada Lagna (Marriage Point) falls in {RASHI_NAMES[ul_rashi]}, defining the external circumstances of marriage."
        ))

        # Check for stability of UL (2nd from UL)
        ul_2nd_rashi = (ul_rashi + 1) % 12
        benefics = ["Jupiter", "Venus", "Mercury", "Moon"]
        stable = any(p.rashi == ul_2nd_rashi and name in benefics for name, p in planets.items())
        if stable:
            factors.append(EvidenceEngine.create_factor(
                "Spousal Support", "house", "positive", 15,
                "Strong support for the Upapada Lagna indicates a stable and enduring marital bond."
            ))

    # B. Darakaraka (DK)
    dk_name = chart.jaimini_karakas.get("Darakaraka (DK) - Spouse")
    if dk_name:
        dk = planets[dk_name]
        factors.append(EvidenceEngine.create_factor(
            "Darakaraka", "planet", "positive" if dk.house not in [6, 8, 12] else "neutral", 10,
            f"{dk_name} is your Darakaraka (Spouse Indicator). Its strength and placement define your partner's core traits."
        ))

    # C. Natural Indicators
    # Passion (Venus-Mars)
    if are_associated("Venus", "Mars", planets):
        factors.append(EvidenceEngine.create_factor("Relational Intensity", "yoga", "positive", 10, "A connection between Venus and Mars indicates a passionate and energetic approach to relationships."))

    # Relational Style
    styles = {
        "Sun": "Respect-driven and authoritative",
        "Moon": "Nurturing and emotionally deep",
        "Mars": "Action-oriented and protective",
        "Mercury": "Communication-focused and intellectual",
        "Jupiter": "Wisdom-based and growth-oriented",
        "Venus": "Harmony-driven and aesthetic",
        "Saturn": "Commitment-heavy and traditional",
        "Rahu": "Unconventional and boundary-breaking",
        "Ketu": "Spiritual and slightly detached"
    }
    main_style = seventh_lord_name
    factors.append(EvidenceEngine.create_factor(
        "Relational Style", "lord", "positive", 10,
        f"Your approach to long-term bonds is {styles.get(main_style, 'Balanced')}, as influenced by {main_style}."
    ))

    # Delay/Stability (Saturn on 7th)
    if seventh_lord_name == "Saturn" or planets["Saturn"].house == 7:
        factors.append(EvidenceEngine.create_factor("Relational Maturity", "planet", "neutral", 8, "Saturn's influence on the 7th sector suggests stability or potential delays in marital manifestation."))

    # 7. Timing Integration
    t_conf = False
    d_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        d_conf = timing_data.get("dasha_confirmed", False)
        if d_conf:
            factors.append(EvidenceEngine.create_factor("Relationship Activation", "dasha", "positive", 15, "Current dasha period is highly active for relationship manifestation or major developments."))

    summary_template = (
        "Relationship and marriage trajectory is {score}% synchronized. "
        "With {confidence} confidence, the cosmic patterns indicate "
        + ("a period of deepening bonds and potential for long-term commitment." if seventh_lord.house in [1, 4, 7, 10, 5, 9, 11] else "that relational matters require conscious communication and patience to navigate karmic tests.")
    )

    return analyze_domain(
        domain_type,
        factors,
        summary_template,
        varga_data={"confirmed": varga_confirmed},
        dasha_data={"confirmed": d_conf},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
