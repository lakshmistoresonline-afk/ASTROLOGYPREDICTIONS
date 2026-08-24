from typing import Dict, Any, List

# Limb Yogas: Combinations of Tithi, Vara, and Nakshatra
# Amrit Siddhi, Sarvartha Siddhi, Ravi Yoga, etc.

AMRIT_SIDDHI_PAIRS = {
    # Vara: Nakshatra
    "Sunday": ["Hasta"],
    "Monday": ["Mrigashira"],
    "Tuesday": ["Ashwini"],
    "Wednesday": ["Anuradha"],
    "Thursday": ["Pushya"],
    "Friday": ["Revati"],
    "Saturday": ["Rohini"]
}

SARVARTHA_SIDDHI_PAIRS = {
    "Sunday": ["Hasta", "Moola", "Uttarashada", "Uttarabhadrapada", "Uttaraphalguni", "Pushya", "Ashwini"],
    "Monday": ["Rohini", "Mrigashira", "Pushya", "Anuradha", "Shravana"],
    "Tuesday": ["Ashwini", "Kritika", "Ashlesha", "Uttarabhadrapada"],
    "Wednesday": ["Rohini", "Mrigashira", "Ardra", "Anuradha", "Hasta"],
    "Thursday": ["Ashwini", "Punarvasu", "Pushya", "Anuradha", "Revati"],
    "Friday": ["Ashwini", "Bharani", "Ardra", "Punarvasu", "Shravana", "Revati"],
    "Saturday": ["Rohini", "Swati", "Shravana"]
}

def check_limb_yogas(vara_name: str, nak_name: str) -> List[str]:
    yogas = []

    # 1. Amrit Siddhi
    if nak_name in AMRIT_SIDDHI_PAIRS.get(vara_name, []):
        yogas.append("Amrit Siddhi Yoga (Extremely Auspicious)")

    # 2. Sarvartha Siddhi
    if nak_name in SARVARTHA_SIDDHI_PAIRS.get(vara_name, []):
        yogas.append("Sarvartha Siddhi Yoga (Fulfillment of Desires)")

    return yogas
