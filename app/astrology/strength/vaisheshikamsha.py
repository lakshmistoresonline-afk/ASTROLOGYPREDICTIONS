from typing import Dict, List, Any

# Vaisheshikamsha levels (number of vargas in good dignity)
VAISHESHIKAMSHA_LEVELS = {
    2: "Parijata",
    3: "Uttama",
    4: "Gopura",
    5: "Simhasana",
    6: "Paravata",
    7: "Devaloka",
    8: "Brahmaloka",
    9: "Sakravahana",
    10: "Shridhama"
}

def calculate_vaisheshikamsha(planet: str, vargas_rashis: Dict[str, int]) -> Dict[str, Any]:
    """
    Count number of vargas where planet is in Exaltation, Moolatrikona, or Own Sign.
    Standard Shodasha Varga (16) used.
    """
    from .dignity import get_dignity

    count = 0
    good_vargas = []

    for v_name, rashi in vargas_rashis.items():
        # degree proxy 15.0 for varga dignity check
        dig = get_dignity(planet, rashi, 15.0)
        if any(d in dig for d in ["Exalted", "Own Sign", "Moolatrikona"]):
            count += 1
            good_vargas.append(v_name)

    level = VAISHESHIKAMSHA_LEVELS.get(count, "None" if count < 2 else "Shridhama")

    return {
        "count": count,
        "level": level,
        "vargas": good_vargas
    }
