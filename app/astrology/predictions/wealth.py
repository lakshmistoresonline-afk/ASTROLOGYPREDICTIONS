from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_wealth_prediction(chart: CanonicalChart, domain_type: str = "Wealth & Savings", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Wealth & Savings Analysis: 2nd, 5th, 9th, 11th houses and Jupiter."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords
    sav = chart.ashtakavarga.get("SAV", [28] * 12)

    # 1. 2nd HOUSE (SAVINGS)
    l2_name = house_lords[2]
    l2 = planets[l2_name]
    if l2.house in [1, 2, 4, 5, 7, 9, 10, 11]:
        factors.append(EvidenceEngine.create_factor("2nd Lord Placement", "lord", "positive", 10, f"2nd Lord {l2_name} in House {l2.house} indicates good capacity for savings and accumulated wealth."))

    # 2. 11th HOUSE (GAINS)
    l11_name = house_lords[11]
    l11 = planets[l11_name]
    if l11.house in [1, 2, 4, 5, 7, 9, 10, 11]:
        factors.append(EvidenceEngine.create_factor("11th Lord Placement", "lord", "positive", 10, f"11th Lord {l11_name} in House {l11.house} indicates a steady flow of income and fulfillment of goals."))

    # 3. DHANA YOGAS
    for y in chart.yogas:
        if "Dhana Yoga" in y["name"] or "Lakshmi Yoga" in y["name"]:
            factors.append(EvidenceEngine.create_factor("Yoga", "yoga", "positive", 15, f"Presence of {y['name']} indicates significant wealth accumulation potential."))

    # 4. VARGA CONFIRMATION (D2)
    v_conf = False
    if "D2" in chart.divisional_charts:
        v_conf = True
        factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, "Hora (D2) analysis supports wealth accumulation potential."))

    # 4b. Advanced Wealth Indicators
    # A. Indu Lagna (Wealth Point)
    il_lon = chart.special_lagnas.get("Indu Lagna")
    if il_lon is not None:
        il_rashi = int(il_lon // 30)
        from ..core.houses import RASHI_NAMES
        factors.append(EvidenceEngine.create_factor(
            "Indu Lagna", "yoga", "positive", 12,
            f"Indu Lagna falls in {RASHI_NAMES[il_rashi]}, marking a specific sensitive point for prosperity."
        ))
        # Check if benefics are in Indu Lagna
        for p_name, p_info in planets.items():
            if p_info.rashi == il_rashi and p_name in ["Jupiter", "Venus", "Mercury", "Moon"]:
                factors.append(EvidenceEngine.create_factor(
                    "Benefic in Indu Lagna", "planet", "positive", 20,
                    f"{p_name} in Indu Lagna is a powerful indicator of significant wealth and luxury."
                ))

    # B. Arudha 11th (A11) - Sources of Gain
    a11_rashi = chart.arudha_padas.get("A11")
    if a11_rashi is not None:
        from ..core.houses import RASHI_NAMES
        factors.append(EvidenceEngine.create_factor(
            "Arudha 11th", "yoga", "positive", 8,
            f"The Arudha of gains (A11) falls in {RASHI_NAMES[a11_rashi]}, indicating how the world sees your financial success."
        ))

    # C. Supreme Wealth Points
    # Shree Lagna (Wealth Indicator)
    sl_lon = chart.shree_lagna
    if sl_lon:
        sl_rashi = int(sl_lon // 30)
        from ..core.houses import RASHI_NAMES
        factors.append(EvidenceEngine.create_factor(
            "Wealth Seat", "yoga", "positive", 20,
            f"Your Shree Lagna (Seat of Lakshmi) is in {RASHI_NAMES[sl_rashi]}, marking your core financial destiny."
        ))

    # D. Ashtakavarga Pure Points (Shodhya Pinda)
    sp = chart.ashtakavarga.get("ShodhyaPinda", {})
    jup_sp = sp.get("Jupiter", 0)
    if jup_sp > 150:
        factors.append(EvidenceEngine.create_factor("Jupiter Shodhya Pinda", "ashtakavarga", "positive", 12, "Extremely high Shodhya Pinda for Jupiter confirms abundant and pure sources of wealth."))

    # D. BAV Profit vs Loss (H11 vs H12)
    h11_rashi = (asc_rashi + 10) % 12
    h12_rashi = (asc_rashi + 11) % 12
    sav_11 = sav[h11_rashi]
    sav_12 = sav[h12_rashi]
    if sav_11 > sav_12:
        factors.append(EvidenceEngine.create_factor("Profit-Loss Balance", "ashtakavarga", "positive", 10, f"SAV points in 11th ({sav_11}) exceed 12th ({sav_12}), indicating net financial accumulation."))
    else:
        factors.append(EvidenceEngine.create_factor("Profit-Loss Balance", "ashtakavarga", "negative", 8, f"Higher SAV points in 12th ({sav_12}) than 11th ({sav_11}) suggest high expenditure patterns."))

    # 5. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.7:
            factors.append(EvidenceEngine.create_factor("Accumulation Period", "transit", "positive", 10, "Current planetary cycles are supportive for increasing savings and fixed assets."))

    summary_template = domain_type + " strength: {score}%. Confidence: {confidence}."

    return analyze_domain(
        domain_type,
        factors,
        summary_template,
        varga_data={"confirmed": v_conf},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
