from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_finance_prediction(chart: CanonicalChart, domain_type: str = "Finance & Wealth", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Wealth Analysis: 2nd, 11th houses, Jupiter, and D2 (Hora)."""
    factors = []

    planets = chart.planets
    asc_rashi = chart.asc_rashi
    house_lords = chart.house_lords
    sav = chart.ashtakavarga.get("SAV", [28] * 12)

    # 1. 2nd HOUSE (ACCUMULATED WEALTH)
    second_lord_name = house_lords[2]
    second_lord = planets[second_lord_name]

    factors.append(EvidenceEngine.create_factor(
        "2nd Lord Placement", "lord", "positive" if second_lord.house not in [6, 8, 12] else "negative", 10,
        f"2nd Lord {second_lord_name} in House {second_lord.house}: Defines your ability to save and accumulate wealth."
    ))

    # 2. 11th HOUSE (GAINS)
    eleventh_lord_name = house_lords[11]
    eleventh_lord = planets[eleventh_lord_name]

    factors.append(EvidenceEngine.create_factor(
        "11th Lord Placement", "lord", "positive" if eleventh_lord.house not in [6, 8, 12] else "negative", 10,
        f"11th Lord {eleventh_lord_name} in House {eleventh_lord.house}: Indicates your capacity for professional gains."
    ))

    # 3. JUPITER (KARAKA FOR WEALTH)
    jupiter = planets["Jupiter"]
    if "Exalted" in jupiter.dignity:
        factors.append(EvidenceEngine.create_factor("Jupiter Dignity", "planet", "positive", 20, "Jupiter is Exalted: Natural abundance and financial wisdom."))

    # 4. ASHTAKAVARGA
    r2 = (asc_rashi + 1) % 12
    r11 = (asc_rashi + 10) % 12
    if sav[r2] >= 30:
        factors.append(EvidenceEngine.create_factor("SAV 2nd House", "ashtakavarga", "positive", 5, f"High SAV in 2nd house ({sav[r2]}): Strong capacity to retain wealth."))

    # 4a. VARGA (D2 - HORA)
    varga_confirmed = False
    d2 = chart.divisional_charts.get("D2", {})
    if d2:
        # Simple D2 logic: Benefics in Sun's Hora or Malefics in Moon's Hora
        if "Jupiter" in d2 or "Venus" in d2:
            varga_confirmed = True
            factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, "Hora (D2) analysis confirms financial stability and wealth potential."))

    # 4b. Advanced Wealth Layers
    # A. KP House 2 & 11 Significators
    h2_sigs = chart.kp_significators.get(2, {})
    h11_sigs = chart.kp_significators.get(11, {})
    if "A" in h2_sigs and "B" in h11_sigs:
        top_sigs = h2_sigs["A"] + h11_sigs["B"]
        if any(s in ["Jupiter", "Venus", "Mercury"] for s in top_sigs):
            factors.append(EvidenceEngine.create_factor(
                "KP Wealth Support", "planet", "positive", 12,
                "KP analysis confirms powerful significators for accumulation and gains."
            ))

    # B. Punya Saham (Fortune Point)
    p_saham = chart.sahams.get("Punya Saham")
    if p_saham is not None:
        ps_rashi = int(p_saham // 30)
        from ..core.houses import RASHI_NAMES
        factors.append(EvidenceEngine.create_factor(
            "Fortune Point", "yoga", "positive", 10,
            f"Punya Saham in {RASHI_NAMES[ps_rashi]} highlights a specific cosmic sensitive zone for wealth."
        ))

    # C. Indu Lagna (Prosperity Point)
    il_lon = chart.special_lagnas.get("Indu Lagna")
    if il_lon is not None:
        il_rashi = int(il_lon // 30)
        from ..core.houses import RASHI_NAMES
        factors.append(EvidenceEngine.create_factor(
            "Indu Lagna", "yoga", "positive", 12,
            f"Indu Lagna (Wealth Seat) in {RASHI_NAMES[il_rashi]} confirms inherent financial prosperity."
        ))

        # Indu Lagna Lord status
        from ..core.houses import RASHI_LORDS
        il_lord = RASHI_LORDS[il_rashi]
        if planets[il_lord].house in [1, 4, 7, 10, 5, 9, 11]:
            factors.append(EvidenceEngine.create_factor("Wealth Lord Stability", "lord", "positive", 15, f"The lord of your wealth seat ({il_lord}) is well-placed, ensuring steady accumulation."))

    # 5. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.7:
            factors.append(EvidenceEngine.create_factor("Financial High", "transit", "positive", 12, "Current planetary cycles are exceptionally favorable for financial gains and investments."))

    summary_template = (
        "Wealth and finance potential is {score}% aligned. "
        "With {confidence} confidence, the cosmic treasury indicates "
        + ("a significant capacity for wealth accumulation and resource security." if second_lord.house in [1, 4, 7, 10, 5, 9, 11] else "that financial matters require careful budgeting and realistic management to avoid drainage.")
    )

    return analyze_domain(
        "Finance & Wealth",
        factors,
        summary_template,
        varga_data={"confirmed": varga_confirmed},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
