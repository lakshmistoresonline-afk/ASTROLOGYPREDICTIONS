from typing import Dict, List, Any, Optional

def get_numerology_data(birth_date: str) -> Dict[str, Any]:
    """
    Pythagorean and Chaldean Numerology mapping.
    birth_date format: 'YYYY-MM-DD'
    """
    y, m, d = map(int, birth_date.split('-'))

    # 1. Life Path Number (Sum of all digits)
    digits = [int(x) for x in f"{y}{m:02d}{d:02d}"]
    def reduce(n):
        while n > 9 and n not in [11, 22, 33]:
            n = sum(int(x) for x in str(n))
        return n

    lp = reduce(sum(digits))

    # 2. Psychic Number (Day of birth)
    psychic = reduce(d)

    # 3. Destiny Number (Full Name - usually requires name input, placeholder for now)

    # Mapping to Planetary Energy
    PLANET_MAP = {
        1: "Sun", 2: "Moon", 3: "Jupiter", 4: "Rahu",
        5: "Mercury", 6: "Venus", 7: "Ketu", 8: "Saturn", 9: "Mars"
    }

    return {
        "life_path": lp,
        "psychic_number": psychic,
        "primary_planet": PLANET_MAP.get(lp if lp <= 9 else lp // 11), # Simplified for Master numbers
        "interpretation": f"Your Life Path {lp} resonates with the energy of {PLANET_MAP.get(lp, 'Advanced Energy')}."
    }

def get_lo_shu_grid(birth_date: str) -> List[List[Optional[int]]]:
    """3x3 Lo Shu Grid (Feng Shui Numerology)."""
    y, m, d = map(int, birth_date.split('-'))
    s = f"{y}{m:02d}{d:02d}"
    counts = {int(x): s.count(x) for x in "123456789"}

    # Grid Layout:
    # 4 9 2
    # 3 5 7
    # 8 1 6
    grid = [
        [4 if counts[4] else None, 9 if counts[9] else None, 2 if counts[2] else None],
        [3 if counts[3] else None, 5 if counts[5] else None, 7 if counts[7] else None],
        [8 if counts[8] else None, 1 if counts[1] else None, 6 if counts[6] else None]
    ]
    return grid
