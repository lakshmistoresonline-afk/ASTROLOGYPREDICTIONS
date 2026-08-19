from typing import List, Dict
from ..core.models import CanonicalChart

REMEDIES_DATABASE = {
    "Sun": {
        "mantra": "Om Ghrini Suryaya Namah",
        "charity": "Donate wheat, jaggery, or copper on Sundays.",
        "lifestyle": "Wake up before sunrise, offer water to the Sun (Arghya)."
    },
    "Moon": {
        "mantra": "Om Shram Shreem Shraum Sah Chandramase Namah",
        "charity": "Donate rice, milk, or white clothes on Mondays.",
        "lifestyle": "Practice meditation, stay hydrated, respect maternal figures."
    },
    "Mars": {
        "mantra": "Om Kram Kreem Kraum Sah Bhaumaya Namah",
        "charity": "Donate red lentils (Masoor Dal) or red clothes on Tuesdays.",
        "lifestyle": "Physical exercise, avoid spicy food, maintain discipline."
    },
    "Mercury": {
        "mantra": "Om Bram Breem Braum Sah Budhaya Namah",
        "charity": "Donate green gram (Moong Dal) or green clothes on Wednesdays.",
        "lifestyle": "Read books, practice clear communication, avoid lying."
    },
    "Jupiter": {
        "mantra": "Om Gram Greem Graum Sah Gurave Namah",
        "charity": "Donate chickpeas, turmeric, or yellow clothes on Thursdays.",
        "lifestyle": "Seek wisdom from elders, practice gratitude, study spiritual texts."
    },
    "Venus": {
        "mantra": "Om Dram Dreem Draum Sah Shukraya Namah",
        "charity": "Donate curd, sugar, or white sweets on Fridays.",
        "lifestyle": "Maintain cleanliness, appreciate art, respect life partners."
    },
    "Saturn": {
        "mantra": "Om Pram Preem Praum Sah Shanaishcharaya Namah",
        "charity": "Donate black sesame, mustard oil, or iron items on Saturdays.",
        "lifestyle": "Be humble, serve the needy, practice patience and hard work."
    },
    "Rahu": {
        "mantra": "Om Bhram Bhreem Bhraum Sah Rahave Namah",
        "charity": "Donate urad dal or coconut on Saturdays.",
        "lifestyle": "Avoid addictions, practice yoga, stay grounded in reality."
    },
    "Ketu": {
        "mantra": "Om Sram Sreem Sraum Sah Ketave Namah",
        "charity": "Donate multi-colored blankets or items on Tuesdays.",
        "lifestyle": "Practice introspection, detachment from material results."
    }
}

def get_remedies(chart: CanonicalChart) -> List[Dict]:
    """Identify planets needing remedies and suggest Upayas."""
    remedies = []

    # 1. Check for Debilitated planets
    for name, p in chart.planets.items():
        if "Debilitated" in p.dignity:
            db_rem = REMEDIES_DATABASE.get(name, {})
            remedies.append({
                "planet": name,
                "reason": "Debilitated (Weak Status)",
                "mantra": db_rem.get("mantra"),
                "charity": db_rem.get("charity"),
                "lifestyle": db_rem.get("lifestyle")
            })

        # 2. Check for Combust planets
        elif p.is_combust:
            cb_rem = REMEDIES_DATABASE.get(name, {})
            remedies.append({
                "planet": name,
                "reason": "Combust (Burnt by Sun)",
                "mantra": cb_rem.get("mantra"),
                "charity": cb_rem.get("charity"),
                "lifestyle": cb_rem.get("lifestyle")
            })

    # 3. Functional Malefics in difficult houses (6, 8, 12)
    for name, p in chart.planets.items():
        if p.functional_status == "Functional Malefic" and p.house in [6, 8, 12]:
            # Avoid duplicate if already added for debilitation
            if not any(r["planet"] == name for r in remedies):
                fm_rem = REMEDIES_DATABASE.get(name, {})
                remedies.append({
                    "planet": name,
                    "reason": f"Functional Malefic in House {p.house}",
                    "mantra": fm_rem.get("mantra"),
                    "charity": fm_rem.get("charity"),
                    "lifestyle": fm_rem.get("lifestyle")
                })

    return remedies
