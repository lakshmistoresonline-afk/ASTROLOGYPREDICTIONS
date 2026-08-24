from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_education_prediction(chart: CanonicalChart, domain_type: str = "Education & Knowledge", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Academic Analysis: Houses (2, 4, 5, 9), Mercury, Jupiter, and D24."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords
    sav = chart.ashtakavarga.get("SAV", [28] * 12)
    asc_rashi = chart.asc_rashi

    # 1. Primary Academic Houses
    # House 4 (General Education), House 5 (Intelligence)
    h4_lord = house_lords[4]
    h5_lord = house_lords[5]

    factors.append(EvidenceEngine.create_factor(
        "Academic Foundation", "lord", "positive" if planets[h4_lord].house not in [6, 8, 12] else "negative", 12,
        f"4th Lord {h4_lord} in House {planets[h4_lord].house}: Stability in formal schooling."
    ))

    factors.append(EvidenceEngine.create_factor(
        "Intelligence Factor", "lord", "positive" if planets[h5_lord].house not in [6, 8, 12] else "negative", 15,
        f"5th Lord {h5_lord} in House {planets[h5_lord].house}: Creative intelligence and focus."
    ))

    # 2. Karakas: Mercury (Logic) and Jupiter (Wisdom)
    mercury = planets["Mercury"]
    jupiter = planets["Jupiter"]

    if "Exalted" in mercury.dignity or mercury.house in [1, 4, 5, 10]:
        factors.append(EvidenceEngine.create_factor("Intellectual Sharpness", "planet", "positive", 12, "Strong Mercury provides analytical skills and academic proficiency."))
    elif "Debilitated" in mercury.dignity:
        factors.append(EvidenceEngine.create_factor("Learning Challenges", "planet", "negative", 10, "Mercury debility may cause hurdles in communication or logical grasp."))

    if jupiter.house in [5, 9, 11] or "Exalted" in jupiter.dignity:
        factors.append(EvidenceEngine.create_factor("Higher Wisdom", "planet", "positive", 10, "Jupiter support indicates success in higher education and deep knowledge."))

    # 3. Ashtakavarga support in 5th House
    h5_rashi = (asc_rashi + 4) % 12
    if sav[h5_rashi] >= 30:
        factors.append(EvidenceEngine.create_factor("Intelligence SAV", "ashtakavarga", "positive", 8, f"High SAV ({sav[h5_rashi]}) in 5th house strengthens academic focus."))

    # 4. Varga Confirmation (D24 - Siddhamsha)
    varga_confirmed = False
    d24 = chart.divisional_charts.get("D24", {})
    if d24:
        d24_lagna = d24.get("Lagna", 0)
        d24_h5_lord = d24.get(h5_lord)
        if d24_h5_lord is not None:
            rel_h = (d24_h5_lord - d24_lagna + 12) % 12 + 1
            if rel_h in [1, 4, 5, 7, 9, 10]:
                varga_confirmed = True
                factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, "Strong D24 placement confirms advanced learning capabilities."))

        # Saraswati Yoga check in D24
        d24_merc = d24.get("Mercury")
        d24_jup = d24.get("Jupiter")
        d24_ven = d24.get("Venus")
        if d24_merc is not None and d24_jup is not None and d24_ven is not None:
            houses = [(r - d24_lagna + 12) % 12 + 1 for r in [d24_merc, d24_jup, d24_ven]]
            if all(h in [1, 4, 7, 10, 5, 9] for h in houses):
                factors.append(EvidenceEngine.create_factor("Siddhamsha Yoga", "varga", "positive", 15, "A version of Saraswati Yoga is present in D24, indicating mastery over specialized knowledge."))

    # 4b. Advanced Knowledge Indicators
    # A. Vidya Saham (Education Point)
    vidya_lon = chart.sahams.get("Vidya Saham")
    if vidya_lon is not None:
        vidya_rashi = int(vidya_lon // 30)
        from ..core.houses import RASHI_NAMES
        factors.append(EvidenceEngine.create_factor(
            "Vidya Saham", "yoga", "positive", 8,
            f"Vidya Saham (Education Point) in {RASHI_NAMES[vidya_rashi]} pinpoints your unique academic strength."
        ))

    # B. KP House 4 Significators
    h4_sigs = chart.kp_significators.get(4, {})
    if "A" in h4_sigs and "B" in h4_sigs:
        top_sigs = h4_sigs["A"] + h4_sigs["B"]
        if "Jupiter" in top_sigs or "Mercury" in top_sigs:
            factors.append(EvidenceEngine.create_factor(
                "KP Education Support", "planet", "positive", 12,
                "KP analysis confirms strong significators for formal education and knowledge acquisition."
            ))

    # 5. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.6:
            factors.append(EvidenceEngine.create_factor("Academic Window", "dasha", "positive", 10, "Current planetary cycles are highly supportive for exams, certifications, or new learning."))

    summary_template = domain_type + " potential: {score}%. Confidence: {confidence}."

    return analyze_domain(
        domain_type,
        factors,
        summary_template,
        varga_data={"confirmed": varga_confirmed},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
