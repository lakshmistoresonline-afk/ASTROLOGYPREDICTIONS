from typing import Dict, Any, List

def calculate_baladi_avastha(rashi: int, degree: float) -> str:
    """
    Baladi Avastha (Age-based state):
    Odd signs: 0-6 Bala (Infant), 6-12 Kumara (Youth), 12-18 Yuva (Adult), 18-24 Vriddha (Old), 24-30 Mrita (Dead).
    Even signs: Reverse order.
    """
    is_odd = rashi % 2 == 0 # 0=Aries (Odd sign)

    idx = int(degree / 6)
    if idx > 4: idx = 4

    states = ["Bala (Infant)", "Kumara (Youth)", "Yuva (Adult)", "Vriddha (Old)", "Mrita (Dead)"]
    if not is_odd:
        states = states[::-1]

    return states[idx]

def calculate_lajjitadi_avastha(planet: str, rashi: int, occupants: List[str], house: int, dignity: str) -> List[str]:
    """
    Lajjitadi Avasthas (Feelings-based states):
    Lajjit (Shame), Garvit (Pride), Kshudhit (Hungry), Trishit (Thirsty), Mudit (Happy), Kshobhit (Agitated).
    """
    states = []

    # 1. Lajjit: In 5th house with Rahu/Ketu or Sun/Sat/Mars
    if house == 5 and any(p in occupants for p in ["Rahu", "Ketu", "Sun", "Saturn", "Mars"]):
        states.append("Lajjit (Shame)")

    # 2. Garvit: In Exaltation or Moolatrikona
    if "Exalted" in dignity or "Moolatrikona" in dignity:
        states.append("Garvit (Pride)")

    # 3. Kshudhit: In Enemy sign or conjunct/aspected by Saturn/Mars
    if "Enemy" in dignity or any(p in occupants for p in ["Saturn", "Mars"]):
        states.append("Kshudhit (Hungry)")

    # 4. Trishit: In Water sign (Cancer, Scorpio, Pisces) aspected by malefic
    if rashi in [3, 7, 11] and any(p in occupants for p in ["Saturn", "Mars", "Sun"]):
        states.append("Trishit (Thirsty)")

    # 5. Mudit: In Friend's sign, with Jupiter, or in Exaltation
    if "Jupiter" in occupants or "Friend" in dignity:
        states.append("Mudit (Happy)")

    # 6. Kshobhit: With Sun and aspected by/with Saturn/Mars
    if "Sun" in occupants and any(p in occupants for p in ["Saturn", "Mars"]):
        states.append("Kshobhit (Agitated)")

    return states

def calculate_shayanadi_avastha(planet_num: int, moon_nak_idx: int, lagna_idx: int, birth_time_ghati: float) -> str:
    """
    Shayanadi Avasthas (12 states):
    Shayana (Sleep), Upaveshana (Sitting), Netrapani, Prakashana, Gamana...
    Formula involving Planet No, Moon Nak, Ghati, etc.
    """
    # Placeholder for complex formula
    # S = (P * N * G + L) % 12
    states = [
        "Shayana", "Upaveshana", "Netrapani", "Prakashana", "Gamana", "Agamana",
        "Sabha", "Agama", "Bhojana", "Nrityalipsa", "Kautuka", "Nidra"
    ]
    idx = (planet_num * (moon_nak_idx + 1)) % 12
    return states[idx]

def calculate_deeptadi_avastha(planet: str, dignity: str) -> str:
    """
    Deeptadi Avasthas (9 types):
    1. Deept (Exaltation)
    2. Swastha (Own Sign)
    3. Mudit (Great Friend)
    4. Shanta (Friend)
    5. Deena (Neutral)
    6. Dukhita (Enemy)
    7. Vikala (Combust)
    8. Khala (Great Enemy)
    9. Kopita (Debilitation)
    """
    # dignity maps: 'Exalted', 'Own Sign', 'Moolatrikona', 'Great Friend', 'Friend', 'Neutral', 'Enemy', 'Great Enemy', 'Debilitated'
    mapping = {
        "Exalted": "Deept (Bright/Exalted)",
        "Own Sign": "Swastha (Content/Own Sign)",
        "Moolatrikona": "Swastha (Content)",
        "Great Friend": "Mudit (Happy)",
        "Friend": "Shanta (Peaceful)",
        "Neutral": "Deena (Sad/Neutral)",
        "Enemy": "Dukhita (Distressed/Enemy)",
        "Great Enemy": "Khala (Mischievous)",
        "Debilitated": "Kopita (Angry/Debilitated)"
    }
    return mapping.get(dignity, "Deena (Neutral)")
