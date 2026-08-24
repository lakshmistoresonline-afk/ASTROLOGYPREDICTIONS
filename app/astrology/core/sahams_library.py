from typing import Dict, Any

def calculate_extended_sahams(planets: Dict[str, Any], asc_lon: float, is_day: bool) -> Dict[str, float]:
    """
    Arabic Parts / Sahams expanded library.
    Formula: A - B + C
    """
    def calc(a, b, c): return (a - b + c) % 360

    p = {name: info.longitude for name, info in planets.items() if hasattr(info, 'longitude')}
    if not p: return {}

    sahams = {}

    # Material
    sahams["Success"] = calc(p["Jupiter"], p["Sun"], asc_lon) if is_day else calc(p["Sun"], p["Jupiter"], asc_lon)
    sahams["Trade"] = calc(p["Mercury"], p["Sun"], asc_lon) if is_day else calc(p["Sun"], p["Mercury"], asc_lon)
    sahams["Agriculture"] = calc(p["Saturn"], p["Venus"], asc_lon)

    # Health/Spirit
    sahams["Sickness"] = calc(p["Mars"], p["Saturn"], asc_lon)
    sahams["Death"] = calc(p[list(planets.keys())[7] if len(planets)>7 else "Saturn"], p["Moon"], p["Saturn"]) # 8th house cusp?

    # Social
    sahams["Father"] = calc(p["Sun"], p["Saturn"], asc_lon) if is_day else calc(p["Saturn"], p["Sun"], asc_lon)
    sahams["Mother"] = calc(p["Moon"], p["Venus"], asc_lon) if is_day else calc(p["Venus"], p["Moon"], asc_lon)
    sahams["Brothers"] = calc(p["Jupiter"], p["Saturn"], asc_lon)

    # Desires
    sahams["Desire"] = calc(p["Mars"], p["Sun"], p["Moon"])
    sahams["Passion"] = calc(p["Mars"], p["Venus"], asc_lon)

    # Professional
    sahams["Action/Career"] = calc(p["Mars"], p["Sun"], asc_lon) if is_day else calc(p["Sun"], p["Mars"], asc_lon)

    # Expanded Library
    sahams["Marriage (Traditional)"] = calc(p["Jupiter"], p["Mars"], asc_lon)
    sahams["Marriage (Modern)"] = calc(p["Venus"], p["Saturn"], asc_lon)
    sahams["Abundance"] = calc(p["Sun"], p["Jupiter"], p["Moon"])
    sahams["Fame"] = calc(p["Jupiter"], p["Sun"], p["Moon"])
    sahams["Honor"] = calc(p["Sun"], p["Jupiter"], asc_lon)
    sahams["Art/Beauty"] = calc(p["Venus"], p["Sun"], asc_lon)
    sahams["Debt"] = calc(p["Saturn"], p["Mars"], asc_lon)
    sahams["Enemies"] = calc(p["Mars"], p["Saturn"], asc_lon)
    sahams["Friendship"] = calc(p["Moon"], p["Jupiter"], asc_lon)
    sahams["Inheritance"] = calc(p["Moon"], p["Saturn"], p["Jupiter"])
    sahams["Sudden Luck"] = calc(p["Jupiter"], p["Mars"], p["Sun"])
    sahams["Wisdom"] = calc(p["Jupiter"], p["Sun"], p["Saturn"])
    sahams["Speculation"] = calc(p["Jupiter"], p["Sun"], p["Mars"])
    sahams["Legal Matters"] = calc(p["Jupiter"], p["Mars"], p["Mercury"])
    sahams["Business Partnerships"] = calc(p["Mercury"], p["Sun"], p["Venus"])

    return sahams
