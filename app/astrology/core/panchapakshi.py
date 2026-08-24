from typing import Dict, List, Any

# Birds in order
BIRDS = ["Vulture", "Owl", "Crow", "Cock", "Peacock"]

# Nakshatra to Bird mapping (Shukla Paksha)
NAK_TO_BIRD_SHUKLA = {
    1: 0, 2: 0, 3: 0, 4: 0, 5: 0,
    6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1,
    12: 2, 13: 2, 14: 2, 15: 2, 16: 2,
    17: 3, 18: 3, 19: 3, 20: 3, 21: 3,
    22: 4, 23: 4, 24: 4, 25: 4, 26: 4, 27: 4
}

# (KRISHNA PAKSHA is different)
NAK_TO_BIRD_KRISHNA = {
    1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3,
    7: 4, 8: 4, 9: 4, 10: 4, 11: 4, 12: 4,
    13: 0, 14: 0, 15: 0, 16: 0, 17: 0,
    18: 1, 19: 1, 20: 1, 21: 1, 22: 1,
    23: 2, 24: 2, 25: 2, 26: 2, 27: 2
}

def get_panchapakshi_info(nak_num: int, is_shukla: bool) -> str:
    """Return the native's bird."""
    mapping = NAK_TO_BIRD_SHUKLA if is_shukla else NAK_TO_BIRD_KRISHNA
    idx = mapping.get(nak_num, 0)
    return BIRDS[idx]

def get_current_activity(bird: str, weekday: int, segment: int) -> str:
    """
    segment: 0-4 (day segments)
    Returns Eating, Walking, Ruling, Sleeping, Dying.
    """
    from .panchapakshi_data import get_segment_activity
    return get_segment_activity(bird, weekday, segment)
