from typing import Dict, Any, List

def calculate_varga_rashi(longitude: float, division: int) -> int:
    """
    Calculate the rashi index for a given division.
    Standard algorithm for many vargas.
    """
    rashi = int(longitude // 30)
    degree_in_rashi = longitude % 30

    # Position in divisions (0-indexed)
    div_idx = int(degree_in_rashi / (30 / division))

    if division == 9: # Navamsa
        # Fire signs: starts from Aries (0)
        # Earth signs: starts from Capricorn (9)
        # Air signs: starts from Libra (6)
        # Water signs: starts from Cancer (3)
        starts = [0, 9, 6, 3]
        start = starts[rashi % 4]
        return (start + div_idx) % 12

    if division == 10: # Dashamsha
        # Odd signs: starts from same sign
        # Even signs: starts from 9th sign
        if rashi % 2 == 0: # Odd sign (0=Aries, 1=Taurus...) wait, 0 is odd in counting
            # Vedic counts: Aries=1 (Odd), Taurus=2 (Even)
            # My index: 0=Aries (Odd), 1=Taurus (Even)
            start = rashi
        else:
            start = (rashi + 8) % 12
        return (start + div_idx) % 12

    # Default fallback for simple divisions (like D1)
    return (rashi * division + div_idx) % 12

def get_varga_chart(planets_lon: Dict[str, float], ascendant_lon: float, division: int) -> Dict[str, int]:
    """Calculate all positions for a specific Varga chart."""
    varga = {}
    varga["Lagna"] = calculate_varga_rashi(ascendant_lon, division)
    for p, lon in planets_lon.items():
        varga[p] = calculate_varga_rashi(lon, division)
    return varga
