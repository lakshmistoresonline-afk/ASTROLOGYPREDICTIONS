from typing import List, Dict, Any

def get_graha_drishti(planet: str, rashi_idx: int) -> List[int]:
    """Return a list of Rashi indices that the planet aspects."""
    # All planets aspect the 7th sign from their position
    aspects = [(rashi_idx + 6) % 12]

    # Special aspects
    if planet == "Mars":
        aspects.append((rashi_idx + 3) % 12) # 4th
        aspects.append((rashi_idx + 7) % 12) # 8th
    elif planet == "Jupiter":
        aspects.append((rashi_idx + 4) % 12) # 5th
        aspects.append((rashi_idx + 8) % 12) # 9th
    elif planet == "Saturn":
        aspects.append((rashi_idx + 2) % 12) # 3rd
        aspects.append((rashi_idx + 9) % 12) # 10th
    elif planet in ["Rahu", "Ketu"]:
        aspects.append((rashi_idx + 4) % 12)
        aspects.append((rashi_idx + 8) % 12)

    return list(set(aspects))

def get_aspect_analysis(planets: Dict[str, Any], asc_rashi: int) -> List[Dict[str, Any]]:
    """Generate detailed insights about planetary aspects."""
    insights = []

    for p_name, p_data in planets.items():
        if p_name in ["Rahu", "Ketu"]: continue # Standard drishtis only

        rashi = p_data.rashi if hasattr(p_data, 'rashi') else p_data.get('rashi')
        drishtis = get_graha_drishti(p_name, rashi)

        for target_rashi in drishtis:
            # Find planets in target rashi
            for o_name, o_data in planets.items():
                o_rashi = o_data.rashi if hasattr(o_data, 'rashi') else o_data.get('rashi')
                if o_rashi == target_rashi:
                    # Aspect formed
                    target_house = (target_rashi - asc_rashi + 12) % 12 + 1
                    insights.append({
                        "from": p_name,
                        "to": o_name,
                        "house": target_house,
                        "type": "Full Aspect",
                        "impact": _get_aspect_impact(p_name, o_name)
                    })
    return insights

def _get_aspect_impact(p1: str, p2: str) -> str:
    # Simplified impact
    benefics = ["Jupiter", "Venus", "Moon", "Mercury"]
    if p1 == "Jupiter": return f"Divine grace of Jupiter expands the qualities of {p2}."
    if p1 == "Saturn": return f"Saturn's gaze brings discipline and restriction to {p2}."
    if p1 == "Mars": return f"Mars adds energy and potential friction to {p2}."
    if p1 in benefics: return f"Benefic {p1} supports and nourishes {p2}."
    return f"{p1} influences {p2}."
