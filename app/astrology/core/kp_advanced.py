from .kp import get_kp_lords
from typing import Dict, List, Any

def calculate_kp_4_steps(chart: Any) -> Dict[str, Dict[str, List[int]]]:
    """
    KP 4-Step Theory for Planet-to-House significance.
    Step 1: Planet itself
    Step 2: Star Lord of the Planet
    Step 3: Sub Lord of the Planet
    Step 4: Star Lord of the Sub Lord
    """
    planets = chart.planets
    house_lords = chart.house_lords
    results = {}

    # Pre-calculate lords for all planets
    planet_kp = {}
    for p_name, p_info in planets.items():
        star, sub = get_kp_lords(p_info.longitude)
        # Star Lord of Sub Lord
        sub_info = planets.get(sub)
        if sub_info:
            sub_star, _ = get_kp_lords(sub_info.longitude)
        else:
            sub_star = sub # Fallback

        planet_kp[p_name] = {
            "Star": star,
            "Sub": sub,
            "SubStar": sub_star
        }

    for p_name, p_info in planets.items():
        kp = planet_kp[p_name]

        # Step 1: Planet
        step1 = [p_info.house]

        # Step 2: Star Lord
        sl_name = kp["Star"]
        sl_info = planets.get(sl_name)
        step2 = [sl_info.house] if sl_info else []

        # Step 3: Sub Lord
        sub_name = kp["Sub"]
        sub_info = planets.get(sub_name)
        step3 = [sub_info.house] if sub_info else []

        # Step 4: Star Lord of Sub Lord
        ss_name = kp["SubStar"]
        ss_info = planets.get(ss_name)
        step4 = [ss_info.house] if ss_info else []

        results[p_name] = {
            "Step 1 (Planet)": step1,
            "Step 2 (Star Lord)": step2,
            "Step 3 (Sub Lord)": step3,
            "Step 4 (Star Lord of Sub)": step4
        }

    return results

def get_house_significators(chart: Any) -> Dict[int, List[str]]:
    """
    Calculate KP Significators for each house (Levels A, B, C, D).
    A: Planets in Star of Planet in House
    B: Planets in the House
    C: Planets in Star of House Lord
    D: House Lord
    """
    res = {i: [] for i in range(1, 13)}
    planets = chart.planets

    # Level B: Planets in the House
    for p_name, p_info in planets.items():
        res[p_info.house].append(p_name)

    # Level D: House Lord
    for h, lord in chart.house_lords.items():
        if lord not in res[h]:
            res[h].append(lord)

    # Level C: Planets in Star of House Lord
    for p_name, p_info in planets.items():
        star, _ = get_kp_lords(p_info.longitude)
        for h, lord in chart.house_lords.items():
            if star == lord:
                if p_name not in res[h]:
                    res[h].append(p_name)

    return res
