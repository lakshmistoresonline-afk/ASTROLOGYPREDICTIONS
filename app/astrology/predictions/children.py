from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_children_prediction(chart: CanonicalChart, domain_type: str = "Children & Successors", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Progeny Analysis: 5th House, Jupiter, and D7 (Saptamsha)."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. 5th HOUSE (CHILDREN)
    l5_name = house_lords[5]
    l5 = planets[l5_name]
    factors.append(EvidenceEngine.create_factor(
        "5th Lord Placement", "lord", "positive" if l5.house not in [6, 8, 12] else "negative", 10,
        f"5th Lord {l5_name} in House {l5.house}: Defines your experience with progeny and creativity."
    ))

    # 2. JUPITER (KARAKA FOR CHILDREN)
    jupiter = planets["Jupiter"]
    if "Exalted" in jupiter.dignity or jupiter.dignity == "Own Sign":
        factors.append(EvidenceEngine.create_factor("Jupiter Strength", "planet", "positive", 15, "Strong Jupiter: Traditionally favorable for happiness through children."))
    elif "Debilitated" in jupiter.dignity:
        factors.append(EvidenceEngine.create_factor("Jupiter Strength", "planet", "negative", 10, "Weak Jupiter: May indicate delays or higher responsibilities regarding children."))

    # 3. D7 CONFIRMATION
    varga_confirmed = False
    d7 = chart.divisional_charts.get("D7", {})
    if d7:
        d7_lagna = d7.get("Lagna", 0)
        d7_pos = d7.get(l5_name)
        if d7_pos is not None:
            rel_h = (d7_pos - d7_lagna + 12) % 12 + 1
            if rel_h in [1, 4, 5, 7, 9, 10]:
                varga_confirmed = True
                factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 12, f"5th Lord in a favorable house (H{rel_h}) in Saptamsha (D7)."))

    # 3b. Advanced Jaimini Progeny Insights
    # A. Putrakaraka (PK)
    pk_name = chart.jaimini_karakas.get("Putrakaraka (PK) - Children")
    if pk_name:
        pk = planets[pk_name]
        factors.append(EvidenceEngine.create_factor(
            "Putrakaraka", "planet", "positive" if pk.house not in [6, 8, 12] else "neutral", 15,
            f"{pk_name} is your Putrakaraka. Its placement in House {pk.house} defines the happiness and creativity you derive through successors."
        ))

    # B. Sudarshana Chakra Resonance for 5th House
    s_chakra = chart.sudarshana_chakra.get(5, {})
    if s_chakra.get("resonance") == "HIGH":
        factors.append(EvidenceEngine.create_factor(
            "Sudarshana Support", "house", "positive", 10,
            "The 5th house is strong from Lagna, Moon, and Sun perspectives, indicating a definitive destiny regarding progeny."
        ))

    # C. Seeds of Creation (Beeja & Kshetra Sphuta)
    # Beeja (Male): Sun + Ven + Jup. Kshetra (Female): Moon + Mars + Jup.
    sun_lon = planets["Sun"].longitude
    moon_lon = planets["Moon"].longitude
    mars_lon = planets["Mars"].longitude
    ven_lon = planets["Venus"].longitude
    jup_lon = planets["Jupiter"].longitude

    beeja = (sun_lon + ven_lon + jup_lon) % 360
    kshetra = (moon_lon + mars_lon + jup_lon) % 360

    b_rashi = int(beeja // 30)
    k_rashi = int(kshetra // 30)

    # Standard rule: Beeja in odd sign and odd navamsha is strong. Kshetra in even.
    if b_rashi % 2 == 0: # 0=Aries (Odd)
        factors.append(EvidenceEngine.create_factor("Beeja Strength", "yoga", "positive", 12, "Biological seeds (Beeja Sphuta) fall in a masculine sign, traditionally strengthening progeny potential."))
    if k_rashi % 2 != 0: # 1=Taurus (Even)
        factors.append(EvidenceEngine.create_factor("Kshetra Strength", "yoga", "positive", 12, "Biological soil (Kshetra Sphuta) falls in a feminine sign, traditionally supporting fruitful manifestation."))

    # 4. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.7:
            factors.append(EvidenceEngine.create_factor("Expansion Period", "transit", "positive", 10, "Current planetary alignments are traditionally supportive for growth in this domain."))

    summary_template = "Progeny and creativity potential: {score}%. Confidence: {confidence}."

    return analyze_domain(
        domain_type,
        factors,
        summary_template,
        varga_data={"confirmed": varga_confirmed},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
