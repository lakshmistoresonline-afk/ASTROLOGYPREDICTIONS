from typing import List, Dict
from ..core.models import CanonicalChart

REMEDIES_DATABASE = {
    "Sun": {
        "mantra": "Om Ghrini Suryaya Namah",
        "charity": "Donate wheat, jaggery, or copper on Sundays.",
        "lifestyle": "Wake up before sunrise, offer water to the Sun (Arghya).",
        "quest": "The Sovereign Path: Practice discipline and lead a team project to strengthen your inner Sun."
    },
    "Moon": {
        "mantra": "Om Shram Shreem Shraum Sah Chandramase Namah",
        "charity": "Donate rice, milk, or white clothes on Mondays.",
        "lifestyle": "Practice meditation, stay hydrated, respect maternal figures.",
        "quest": "The Lunar Anchor: Spend time near water bodies and maintain a journal for emotional clarity."
    },
    "Mars": {
        "mantra": "Om Kram Kreem Kraum Sah Bhaumaya Namah",
        "charity": "Donate red lentils (Masoor Dal) or red clothes on Tuesdays.",
        "lifestyle": "Physical exercise, avoid spicy food, maintain discipline.",
        "quest": "The Warrior's Discipline: Engage in high-intensity sports and practice patience in conflicts."
    },
    "Mercury": {
        "mantra": "Om Bram Breem Braum Sah Budhaya Namah",
        "charity": "Donate green gram (Moong Dal) or green clothes on Wednesdays.",
        "lifestyle": "Read books, practice clear communication, avoid lying.",
        "quest": "The Scribe's Journey: Write an article or learn a new technical skill to sharpen your analytical mind."
    },
    "Jupiter": {
        "mantra": "Om Gram Greem Graum Sah Gurave Namah",
        "charity": "Donate chickpeas, turmeric, or yellow clothes on Thursdays.",
        "lifestyle": "Seek wisdom from elders, practice gratitude, study spiritual texts.",
        "quest": "The Sage's Wisdom: Mentor someone younger and visit a place of higher learning."
    },
    "Venus": {
        "mantra": "Om Dram Dreem Draum Sah Shukraya Namah",
        "charity": "Donate curd, sugar, or white sweets on Fridays.",
        "lifestyle": "Maintain cleanliness, appreciate art, respect life partners.",
        "quest": "The Artist's Grace: Decorate your living space and practice an artistic hobby like music or painting."
    },
    "Saturn": {
        "mantra": "Om Pram Preem Praum Sah Shanaishcharaya Namah",
        "charity": "Donate black sesame, mustard oil, or iron items on Saturdays.",
        "lifestyle": "Be humble, serve the needy, practice patience and hard work.",
        "quest": "The Stoic's Endurance: Perform a repetitive, challenging task and volunteer for community service."
    },
    "Rahu": {
        "mantra": "Om Bhram Bhreem Bhraum Sah Rahave Namah",
        "charity": "Donate urad dal or coconut on Saturdays.",
        "lifestyle": "Avoid addictions, practice yoga, stay grounded in reality.",
        "quest": "The Visionary's Clarity: Practice deep breathing and avoid making impulsive unconventional decisions."
    },
    "Ketu": {
        "mantra": "Om Sram Sreem Sraum Sah Ketave Namah",
        "charity": "Donate multi-colored blankets or items on Tuesdays.",
        "lifestyle": "Practice introspection, detachment from material results.",
        "quest": "The Hermit's Insight: Spend a day in complete silence and study a philosophical text."
    }
}

GEMSTONE_DATABASE = {
    "Sun": {"name": "Ruby (Manik)", "finger": "Ring finger", "metal": "Gold", "weight": "5-7 Carats", "time": "Sunday Morning"},
    "Moon": {"name": "Pearl (Moti)", "finger": "Little finger", "metal": "Silver", "weight": "4-6 Carats", "time": "Monday Evening"},
    "Mars": {"name": "Red Coral (Moonga)", "finger": "Ring finger", "metal": "Gold/Copper", "weight": "6-8 Carats", "time": "Tuesday Morning"},
    "Mercury": {"name": "Emerald (Panna)", "finger": "Little finger", "metal": "Gold/Silver", "weight": "3-5 Carats", "time": "Wednesday Morning"},
    "Jupiter": {"name": "Yellow Sapphire (Pukhraj)", "finger": "Index finger", "metal": "Gold", "weight": "5-8 Carats", "time": "Thursday Morning"},
    "Venus": {"name": "Diamond (Heera/Zircon)", "finger": "Middle/Little finger", "metal": "Gold/Platinum", "weight": "1-2 Carats", "time": "Friday Morning"},
    "Saturn": {"name": "Blue Sapphire (Neelam)", "finger": "Middle finger", "metal": "Iron/Gold", "weight": "4-7 Carats", "time": "Saturday Evening"},
    "Rahu": {"name": "Hessonite (Gomed)", "finger": "Middle finger", "metal": "Silver/Gold", "weight": "5-7 Carats", "time": "Saturday Evening"},
    "Ketu": {"name": "Cat's Eye (Lehsunia)", "finger": "Little finger", "metal": "Silver", "weight": "5-7 Carats", "time": "Tuesday Evening"},
}

HERBAL_REMEDIES = {
    "Sun": "Bael root", "Moon": "Khirni root", "Mars": "Anantmool",
    "Mercury": "Vidhara root", "Jupiter": "Banana root", "Venus": "Arand root",
    "Saturn": "Bichu booti", "Rahu": "Chandan", "Ketu": "Ashwagandha"
}

RUDRAKSHA_DATABASE = {
    "Sun": "1 Mukhi (Eka Mukhi) or 12 Mukhi",
    "Moon": "2 Mukhi (Dwi Mukhi)",
    "Mars": "3 Mukhi (Tri Mukhi)",
    "Mercury": "4 Mukhi (Chatur Mukhi)",
    "Jupiter": "5 Mukhi (Pancha Mukhi)",
    "Venus": "6 Mukhi (Shan Mukhi)",
    "Saturn": "7 Mukhi (Sapta Mukhi)",
    "Rahu": "8 Mukhi (Ashta Mukhi)",
    "Ketu": "9 Mukhi (Nava Mukhi)"
}

def get_remedies(chart: CanonicalChart) -> List[Dict]:
    """Identify planets needing remedies and suggest Upayas with Quests."""
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
                "lifestyle": db_rem.get("lifestyle"),
                "quest": db_rem.get("quest"),
                "gemstone": GEMSTONE_DATABASE.get(name),
                "rudraksha": RUDRAKSHA_DATABASE.get(name),
                "herb": HERBAL_REMEDIES.get(name)
            })

        # 2. Check for Combust planets
        elif p.is_combust:
            cb_rem = REMEDIES_DATABASE.get(name, {})
            remedies.append({
                "planet": name,
                "reason": "Combust (Burnt by Sun)",
                "mantra": cb_rem.get("mantra"),
                "charity": cb_rem.get("charity"),
                "lifestyle": cb_rem.get("lifestyle"),
                "quest": cb_rem.get("quest"),
                "gemstone": GEMSTONE_DATABASE.get(name),
                "rudraksha": RUDRAKSHA_DATABASE.get(name)
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
                    "lifestyle": fm_rem.get("lifestyle"),
                    "quest": fm_rem.get("quest")
                })

    # 4. Check for difficult yogas (Kemadruma, etc.)
    for y in chart.yogas:
        if y["name"] == "Kemadruma Yoga":
            moon_rem = REMEDIES_DATABASE.get("Moon", {})
            remedies.append({
                "planet": "Moon",
                "reason": "Kemadruma Yoga (Isolation)",
                "mantra": moon_rem.get("mantra"),
                "charity": "Donate white items to the needy.",
                "lifestyle": "Maintain active social connections, visit Shiva temple.",
                "quest": "The Bridge of Connection: Organize a small gathering or join a community group to overcome inner isolation."
            })

        if "Paapa Kartari" in y["name"]:
            remedies.append({
                "planet": "General",
                "reason": f"Obstruction to House {y['name'][-2]}",
                "mantra": "Om Namo Narayanaya",
                "charity": "Donate food to the hungry.",
                "lifestyle": "Maintain a regular spiritual discipline to build resilience."
            })

    # 5. Upagraha Remedies
    gulika = chart.planets.get("Gulika")
    if gulika and gulika.house in [1, 6, 8, 12]:
        remedies.append({
            "planet": "Saturn",
            "reason": "Gulika Influence (Karmic Pressure)",
            "mantra": "Om Praam Preem Praum Sah Shanaishcharaya Namah",
            "charity": "Donate iron, black oil, or serve the elderly.",
            "lifestyle": "Practice patience and avoid hasty decisions in pressured situations."
        })

    return remedies

def get_lal_kitab_remedies(chart: CanonicalChart) -> List[Dict]:
    """Specific Lal Kitab remedies based on house placements."""
    lk_remedies = []
    planets = chart.planets

    # 1. Teva Classification
    teva_type = "Normal"
    # Blind Teva (Andha Teva): Simplified logic
    if "Sun" in planets and "Saturn" in planets and planets["Sun"].house == planets["Saturn"].house:
         teva_type = "Andha Teva (Blind Chart)"

    # Dharmi Teva: Jupiter in 10th or with Saturn
    sat_h = planets["Saturn"].house if "Saturn" in planets else -1
    if "Jupiter" in planets and (planets["Jupiter"].house == 10 or planets["Jupiter"].house == sat_h):
        teva_type = "Dharmi Teva (Righteous Chart - Protected)"

    # Example Lal Kitab Logic
    # Sun in 10th
    if "Sun" in planets and planets["Sun"].house == 10:
        lk_remedies.append({
            "planet": "Sun",
            "house": 10,
            "remedy": "Avoid wearing blue or black clothes. Do not live in a house facing West.",
            "type": "Lal Kitab"
        })

    # Saturn in 1st
    if "Saturn" in planets and planets["Saturn"].house == 1:
        lk_remedies.append({
            "planet": "Saturn",
            "house": 1,
            "remedy": "Do not build a house before the age of 48. Bury a pot of honey in a deserted place.",
            "type": "Lal Kitab"
        })

    # Mars in 4th
    if "Mars" in planets and planets["Mars"].house == 4:
        lk_remedies.append({
            "planet": "Mars",
            "house": 4,
            "remedy": "Keep an ivory item in the house. Sweeten the milk before drinking.",
            "type": "Lal Kitab"
        })

    # Rahu in 9th
    if "Rahu" in planets and planets["Rahu"].house == 9:
        lk_remedies.append({
            "planet": "Rahu",
            "house": 9,
            "remedy": "Wear a gold chain. Keep a square piece of silver with you.",
            "type": "Lal Kitab"
        })

    return lk_remedies
