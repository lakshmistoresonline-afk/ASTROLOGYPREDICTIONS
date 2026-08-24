from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_parents_prediction(chart: CanonicalChart, domain_type: str = "Parental Support", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Parental Support Analysis: 4th, 9th houses and Sun, Moon, D12."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. 4th HOUSE (MOTHER)
    l4_name = house_lords[4]
    l4 = planets[l4_name]
    factors.append(EvidenceEngine.create_factor(
        "Mother's Support", "lord", "positive" if l4.house not in [6, 8, 12] else "negative", 10,
        f"4th Lord {l4_name} in House {l4.house} indicates the quality of support and happiness from the mother."
    ))

    # 2. 9th HOUSE (FATHER)
    l9_name = house_lords[9]
    l9 = planets[l9_name]
    factors.append(EvidenceEngine.create_factor(
        "Father's Support", "lord", "positive" if l9.house not in [6, 8, 12] else "negative", 10,
        f"9th Lord {l9_name} in House {l9.house} defines the relationship and luck derived from the father."
    ))

    # 3. LUMINARIES (Sun for Father, Moon for Mother)
    sun = planets["Sun"]
    moon = planets["Moon"]
    factors.append(EvidenceEngine.create_factor("Luminary Strength", "planet", "positive", 10, f"Sun (Father) in House {sun.house} and Moon (Mother) in House {moon.house}."))

    # Varga Confirmation (D12)
    varga_confirmed = False
    d12 = chart.divisional_charts.get("D12", {})
    if d12:
        varga_confirmed = True
        factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, "Parental lineage and happiness supported in D12 chart."))

        # Advanced D12: 9th from Sun (Father), 4th from Moon (Mother)
        sun_r = d12.get("Sun")
        moon_r = d12.get("Moon")
        d12_lagna = d12.get("Lagna", 0)

        if sun_r is not None:
            f_r = (sun_r + 8) % 12 # 9th from Sun
            f_h = (f_r - d12_lagna + 12) % 12 + 1
            if f_h in [1, 4, 7, 10, 5, 9]:
                factors.append(EvidenceEngine.create_factor("Father's Legacy", "varga", "positive", 12, "Superior indicators for father's lineage and support in D12."))

        if moon_r is not None:
            m_r = (moon_r + 3) % 12 # 4th from Moon
            m_h = (m_r - d12_lagna + 12) % 12 + 1
            if m_h in [1, 4, 7, 10, 5, 9]:
                factors.append(EvidenceEngine.create_factor("Mother's Legacy", "varga", "positive", 12, "Superior indicators for mother's happiness and lineage in D12."))

    # 4. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.6:
            factors.append(EvidenceEngine.create_factor("Family Period", "transit", "positive", 5, "Current cycles favor family gatherings or events involving parents."))

    summary_template = "Happiness and support from parents: {score}%. Confidence: {confidence}."

    return analyze_domain(
        "Parental Support",
        factors,
        summary_template,
        varga_data={"confirmed": varga_confirmed},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
