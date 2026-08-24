from typing import Dict

# Linear mapping of 64 Hexagrams to the 360 degree circle
HEXAGRAM_NAMES = {
    1: "The Creative", 2: "The Receptive", 3: "Difficulty at the Beginning", 4: "Youthful Folly",
    # ... Simplified for brevity
    64: "Before Completion"
}

def get_hexagram(longitude: float) -> Dict[str, Any]:
    """Calculate the I-Ching Hexagram for a given longitude."""
    # 64 Hexagrams across 360 degrees
    # One hexagram = 5.625 degrees
    hex_num = int(longitude / 5.625) + 1
    if hex_num > 64: hex_num = 64

    return {
        "number": hex_num,
        "name": HEXAGRAM_NAMES.get(hex_num, f"Hexagram {hex_num}"),
        "degree_in_gate": round(longitude % 5.625, 2)
    }
