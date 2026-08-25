from typing import List, Dict, Any
from datetime import datetime, timedelta

def calculate_chara_dasha(asc_rashi: int, planets: Dict[str, Any], birth_dt: datetime = None) -> List[Dict[str, Any]]:
    """
    Jaimini Chara Dasha calculation (KN Rao method).
    Signs are 0-indexed (Aries=0).
    """
    # 1. Dasha Order
    # Forward: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
    # Backward (Indirect): 0, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1

    # Determining Order based on Lagna sign
    # Direct: Aries, Taurus, Gemini, Libra, Scorpio, Sagittarius
    # Indirect: Cancer, Leo, Virgo, Capricorn, Aquarius, Pisces
    direct_signs = [0, 1, 2, 6, 7, 8]

    order = []
    curr = asc_rashi
    is_direct = asc_rashi in direct_signs

    for _ in range(12):
        order.append(curr)
        if is_direct:
            curr = (curr + 1) % 12
        else:
            curr = (curr - 1 + 12) % 12

    # 2. Years for each sign
    dasha_list = []

    # Rashi Lord Mapping
    from ..core.houses import RASHI_LORDS

    for rashi in order:
        lord_name = RASHI_LORDS[rashi]
        # Lord's position
        lord_p = planets.get(lord_name)
        if lord_p is None:
            dasha_list.append({"rashi": rashi, "years": 9}) # Default
            continue

        if isinstance(lord_p, dict):
            lord_rashi = lord_p.get("rashi", 0)
        else:
            # Assume lord_p is the rashi index directly
            lord_rashi = lord_p

        # Years = Distance from Sign to Lord's Sign
        # If Direct sign: count forward
        # If Indirect sign: count backward
        # Exception: Scorpio (Mars/Ketu) and Aquarius (Saturn/Rahu) - Simplified to one lord for now

        dist = 0
        if rashi in [0, 1, 2, 6, 7, 8]: # Direct
            dist = (lord_rashi - rashi + 12) % 12
        else: # Indirect
            dist = (rashi - lord_rashi + 12) % 12

        if dist == 0: dist = 12
        years = dist - 1
        if years == 0: years = 12

        dasha_list.append({
            "rashi": rashi,
            "years": years,
            "name": f"Sign {rashi + 1} Dasha"
        })

    return dasha_list
