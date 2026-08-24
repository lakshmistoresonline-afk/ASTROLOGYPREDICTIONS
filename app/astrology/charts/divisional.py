from typing import Dict

def calculate_varga_rashi(longitude: float, division: int) -> int:
    """
    Calculate the rashi index (0-11) for a given division (Varga).
    """
    rashi = int(longitude // 30)
    degree_in_rashi = longitude % 30
    div_span = 30 / division
    div_idx = int(degree_in_rashi / div_span)

    if division == 1: # D1: Rashi
        return rashi

    if division == 2: # D2: Hora
        # Parashari Hora:
        # Odd signs: Sun (Leo=4) for 1st half, Moon (Cancer=3) for 2nd half.
        # Even signs: Moon (Cancer=3) for 1st half, Sun (Leo=4) for 2nd half.
        is_odd = rashi % 2 == 0 # 0=Aries (Odd), 1=Taurus (Even)... wait, 0 is 1st sign (Odd)
        if is_odd:
            return 4 if div_idx == 0 else 3
        else:
            return 3 if div_idx == 0 else 4

    if division == 3: # D3: Drekkana
        # 1st: Same, 2nd: 5th, 3rd: 9th
        return (rashi + div_idx * 4) % 12

    if division == 4: # D4: Chaturthamsha
        # 1st: Same, 2nd: 4th, 3rd: 7th, 4th: 10th
        return (rashi + div_idx * 3) % 12

    if division == 5: # D5: Panchamsha
        # Odd: Aries(0), Leo(4), Sag(8), Gem(2), Libra(6)
        # Even: Taurus(1), Virgo(5), Cap(9), Cancer(3), Scorp(7)
        is_odd = rashi % 2 == 0
        if is_odd:
            seq = [0, 4, 8, 2, 6]
        else:
            seq = [1, 5, 9, 3, 7]
        return seq[div_idx % 5]

    if division == 6: # D6: Shashtamsha
        # Odd: Starts from Aries(0). Even: Starts from Libra(6).
        is_odd = rashi % 2 == 0
        start = 0 if is_odd else 6
        return (start + div_idx) % 12

    if division == 7: # D7: Saptamsha
        # Odd signs: Starts from same sign
        # Even signs: Starts from 7th sign
        is_odd = rashi % 2 == 0
        start = rashi if is_odd else (rashi + 6) % 12
        return (start + div_idx) % 12

    if division == 8: # D8: Ashtamsha
        # Movable: Aries(0), Fixed: Sag(8), Dual: Leo(4)
        starts = [0, 8, 4]
        start = starts[rashi % 3]
        return (start + div_idx) % 12

    if division == 9: # D9: Navamsha
        # Fire signs: starts from Aries (0)
        # Earth signs: starts from Capricorn (9)
        # Air signs: starts from Libra (6)
        # Water signs: starts from Cancer (3)
        starts = [0, 9, 6, 3]
        start = starts[rashi % 4]
        return (start + div_idx) % 12

    if division == 10: # D10: Dashamsha
        # Odd signs: Starts from same sign
        # Even signs: Starts from 9th sign
        is_odd = rashi % 2 == 0
        start = rashi if is_odd else (rashi + 8) % 12
        return (start + div_idx) % 12

    if division == 11: # D11: Rudramsha
        # Starts from Aries(0) for all, but moves backwards?
        # Common: starts from Aries and moves forward.
        return (0 + div_idx) % 12

    if division == 12: # D12: Dwadashamsha
        # ...
        # Starts from same sign
        return (rashi + div_idx) % 12

    if division == 16: # D16: Shodashamsha
        # Movable signs (0, 3, 6, 9): Aries (0)
        # Fixed signs (1, 4, 7, 10): Leo (4)
        # Dual signs (2, 5, 8, 11): Sagittarius (8)
        starts = [0, 4, 8]
        start = starts[rashi % 3]
        return (start + div_idx) % 12

    if division == 20: # D20: Vimshamsha
        # Movable: Aries (0)
        # Fixed: Sagittarius (8)
        # Dual: Leo (4)
        starts = [0, 8, 4]
        start = starts[rashi % 3]
        return (start + div_idx) % 12

    if division == 24: # D24: Chaturvimshamsha
        # Odd signs: Leo (4)
        # Even signs: Cancer (3)
        is_odd = rashi % 2 == 0
        start = 4 if is_odd else 3
        return (start + div_idx) % 12

    if division == 27: # D27: Saptavimshamsha (Nakshatramsha)
        # Fire signs: Starts from Aries (0)
        # Earth signs: Starts from Cancer (3)
        # Air signs: Starts from Libra (6)
        # Water signs: Starts from Capricorn (9)
        starts = [0, 3, 6, 9]
        start = starts[rashi % 4]
        return (start + div_idx) % 12

    if division == 30: # D30: Trimshamsha
        # Parashari Trimshamsha (Not equal divisions, but degrees assigned to planets/signs)
        # This function usually expects equal divisions. Parashari Trimshamsha is special.
        # Degree assignments:
        # Odd signs: 0-5 Mars (0), 5-10 Saturn (9), 10-18 Jupiter (8), 18-25 Mercury (2), 25-30 Venus (1)
        # Even signs: 0-5 Venus (1), 5-12 Mercury (2), 12-20 Jupiter (8), 20-25 Saturn (9), 25-30 Mars (0)
        # Actually it returns the RASHI index.
        # Odd: Mars (Aries=0), Sat (Aquarius=10), Jup (Sag=8), Merc (Gemini=2), Ven (Libra=6)
        # (Wait, Trimshamsha signs are specific planetary signs)
        is_odd = rashi % 2 == 0
        d = degree_in_rashi
        if is_odd:
            if d < 5: return 0  # Aries
            if d < 10: return 10 # Aquarius
            if d < 18: return 8  # Sagittarius
            if d < 25: return 2  # Gemini
            return 6             # Libra
        else:
            if d < 5: return 1   # Taurus
            if d < 12: return 5  # Virgo
            if d < 20: return 11 # Pisces
            if d < 25: return 9  # Capricorn
            return 7             # Scorpio

    if division == 40: # D40: Khavedamsha
        # Odd: Aries (0), Even: Libra (6)
        is_odd = rashi % 2 == 0
        start = 0 if is_odd else 6
        return (start + div_idx) % 12

    if division == 45: # D45: Akshavedamsha
        # Movable: Aries (0), Fixed: Leo (4), Dual: Sagittarius (8)
        starts = [0, 4, 8]
        start = starts[rashi % 3]
        return (start + div_idx) % 12

    if division == 60: # D60: Shashtiamsha
        # Odd signs (0, 2, 4, 6, 8, 10): Starts from Aries (0)
        # Even signs (1, 3, 5, 7, 9, 11): Starts from Libra (6)
        is_odd = rashi % 2 == 0
        start = 0 if is_odd else 6
        return (start + div_idx) % 12

    # Default fallback: linear division
    return (rashi + div_idx) % 12

def get_varga_chart(planets_lon: Dict[str, float], ascendant_lon: float, division: int) -> Dict[str, int]:
    """Calculate all positions for a specific Varga chart."""
    varga = {}
    varga["Lagna"] = calculate_varga_rashi(ascendant_lon, division)
    for p, lon in planets_lon.items():
        varga[p] = calculate_varga_rashi(lon, division)
    return varga
