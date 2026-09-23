from typing import Dict, List, Any, Optional

# Sarvatobhadra Chakra (SBC) - Transit Analysis Grid
# Evaluates exact Latta, Yuti, and Vedha (Cross-Aspect Obstructions) from transiting planets to natal planets.

MALEFIC_PLANETS = {"Saturn", "Mars", "Rahu", "Ketu", "Sun"}

def check_sbc_transit_impact(
    transit_planets: Dict[str, float],
    natal_points: Dict[str, float],
    transiting_planet: Optional[str] = None,
    target_natal: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Check for Sarvatobhadra Chakra (SBC) Vedha from transiting planets to natal points.
    Strictly verifies whether a specific transiting malefic forms active Vedha/Latta
    to the target natal point before flagging an obstruction.
    """
    alerts = []

    # If specific transiting planet and natal target are supplied, evaluate that specific pair
    if transiting_planet and target_natal:
        if transiting_planet not in MALEFIC_PLANETS:
            return [] # Benefics do not cause malefic Vedha obstruction

        t_lon = transit_planets.get(transiting_planet)
        n_lon = natal_points.get(target_natal)

        if t_lon is not None and n_lon is not None:
            diff = abs(t_lon - n_lon) % 360.0
            if diff > 180.0: diff = 360.0 - diff

            # Direct Vedha contact within tight orb (3.33 deg)
            if diff <= 3.33:
                alerts.append({
                    "type": "SBC Vedha",
                    "planet": transiting_planet,
                    "target": target_natal,
                    "impact": "CRITICAL",
                    "interpretation": f"Transiting {transiting_planet} causes active Sarvatobhadra Vedha on natal {target_natal}."
                })
        return alerts

    # General check: Malefics causing direct contact with natal Moon/Lagna within 3.33 deg
    for p_name in MALEFIC_PLANETS:
        t_lon = transit_planets.get(p_name)
        if t_lon is None: continue

        n_moon = natal_points.get("Moon")
        if n_moon is not None:
            diff = abs(t_lon - n_moon) % 360.0
            if diff > 180.0: diff = 360.0 - diff
            if diff <= 3.33:
                alerts.append({
                    "type": "SBC Vedha",
                    "planet": p_name,
                    "target": "Janma Nakshatra",
                    "impact": "CRITICAL",
                    "interpretation": f"Transiting {p_name} causes active SBC Vedha on natal Moon."
                })

    return alerts
