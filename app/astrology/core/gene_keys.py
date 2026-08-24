from typing import Dict, Any

# Gene Keys mapping (Shadow, Gift, Siddhi)
# Based on the 64 Hexagrams of the I-Ching/Human Design
GENE_KEYS_DATA = {
    1: ("Entropy", "Freshness", "Beauty"),
    2: ("Dislocation", "Orientation", "Unity"),
    25: ("Constriction", "Acceptance", "Universal Love"),
    # ...
}

def get_gene_key_interpretation(gate: int) -> Dict[str, str]:
    data = GENE_KEYS_DATA.get(gate, ("Shadow", "Gift", "Siddhi"))
    return {
        "gate": gate,
        "shadow": data[0],
        "gift": data[1],
        "siddhi": data[2]
    }
