from typing import Dict, List, Any, Optional
import math

# Tajika Aspects (Degrees): 3, 5, 9, 11 (Friendly), 1, 4, 7, 10 (Inimical), 2, 6, 8, 12 (Neutral/No)
TAJIKA_FRIENDLY = [60, 120] # Sextile, Trine (approx)
TAJIKA_INIMICAL = [90, 180, 0] # Square, Opposition, Conjunction

def get_tajika_aspect_type(lon1: float, lon2: float) -> str:
    diff = abs(lon1 - lon2) % 360
    if diff > 180: diff = 360 - diff

    # Orbs (Usually 12 degrees for most planets in Tajika)
    orb = 12.0

    if diff < orb: return "Friendly (Conjunction)" # Conjunction is neutral/variable but treated as association
    if abs(diff - 60) < orb: return "Friendly (Sextile)"
    if abs(diff - 90) < orb: return "Inimical (Square)"
    if abs(diff - 120) < orb: return "Friendly (Trine)"
    if abs(diff - 180) < orb: return "Inimical (Opposition)"

    return "None"

def calculate_tajika_yogas(planets: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Ithasala: Applying aspect between two planets.
    Esharapha: Separating aspect.
    """
    yogas = []
    p_names = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

    for i in range(len(p_names)):
        for j in range(i + 1, len(p_names)):
            p1_name, p2_name = p_names[i], p_names[j]
            p1, p2 = planets[p1_name], planets[p2_name]

            asp = get_tajika_aspect_type(p1.longitude, p2.longitude)
            if asp == "None": continue

            # Check for Ithasala (Applying)
            # Faster planet must be at lower degree and behind the slower planet
            # Speeds: Moon > Merc > Ven > Sun > Mars > Jup > Sat
            SPEED_RANK = {"Moon": 1, "Mercury": 2, "Venus": 3, "Sun": 4, "Mars": 5, "Jupiter": 6, "Saturn": 7}

            f_name, s_name = (p1_name, p2_name) if SPEED_RANK[p1_name] < SPEED_RANK[p2_name] else (p2_name, p1_name)
            fast, slow = planets[f_name], planets[s_name]

            # Simple Ithasala: Fast is behind slow
            is_applying = fast.longitude < slow.longitude

            y_name = "Ithasala Yoga" if is_applying else "Esharapha Yoga"
            strength = "STRONG" if "Friendly" in asp else "CHALLENGING"

            yogas.append({
                "name": f"{y_name} ({f_name} & {s_name})",
                "type": "Tajika",
                "aspect": asp,
                "status": "Applying" if is_applying else "Separating",
                "strength": strength,
                "interpretation": f"{'Productive' if is_applying else 'Declining'} connection between {f_name} and {s_name}."
            })

    return yogas

def calculate_sahams(planets: Dict[str, Any], asc_lon: float, is_day: bool) -> Dict[str, float]:
    """
    Arabic Parts in Vedic.
    Punya Saham (Fortune): Moon - Sun + Asc (Day), Sun - Moon + Asc (Night)
    Vidya Saham (Education): Sun - Moon + Asc (Day), Moon - Sun + Asc (Night)
    """
    sun = planets["Sun"].longitude
    moon = planets["Moon"].longitude

    # Formula: A - B + C
    def calc(a, b, c): return (a - b + c) % 360

    sahams = {}
    if is_day:
        sahams["Punya Saham"] = calc(moon, sun, asc_lon)
        sahams["Vidya Saham"] = calc(sun, moon, asc_lon)
    else:
        sahams["Punya Saham"] = calc(sun, moon, asc_lon)
        sahams["Vidya Saham"] = calc(moon, sun, asc_lon)

    # Additional Sahams
    sahams["Yasha Saham (Fame)"] = calc(planets["Jupiter"].longitude, sahams["Punya Saham"], asc_lon)

    # 1. Rajya Saham (Kingdom/Career)
    sahams["Rajya Saham"] = calc(planets["Saturn"].longitude, planets["Sun"].longitude, asc_lon)
    # 2. Vivaha Saham (Marriage)
    sahams["Vivaha Saham"] = calc(planets["Venus"].longitude, planets["Saturn"].longitude, asc_lon)
    # 3. Putra Saham (Children)
    sahams["Putra Saham"] = calc(planets["Jupiter"].longitude, planets["Sun"].longitude, asc_lon)
    # 4. Shatru Saham (Enemies)
    sahams["Shatru Saham"] = calc(planets["Mars"].longitude, planets["Saturn"].longitude, asc_lon)

    # 5. Vyapara Saham (Business)
    sahams["Vyapara Saham"] = calc(planets["Mars"].longitude, planets["Sun"].longitude, asc_lon)
    # 6. Apasmara Saham (Health/Nerves)
    sahams["Apasmara Saham"] = calc(planets["Mars"].longitude, planets["Moon"].longitude, asc_lon)
    # 7. Kali Saham (Challenges)
    sahams["Kali Saham"] = calc(planets["Saturn"].longitude, planets["Jupiter"].longitude, asc_lon)

    return sahams
