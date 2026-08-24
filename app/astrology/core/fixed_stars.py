from typing import Dict, List, Any

# Major Fixed Stars (Tropical Longitudes for 2026 approx - should be Ayansama adjusted)
# In Vedic, we usually look at Nakshatra padas, but specific star conjunctions are powerful.
FIXED_STARS = [
    {"name": "Regulus", "longitude": 150.0, "nature": "Mars/Jupiter", "effect": "Fame, sudden rise, authority."},
    {"name": "Spica", "longitude": 204.0, "nature": "Venus/Mars", "effect": "Fortune, wealth, artistic success."},
    {"name": "Antares", "longitude": 250.0, "nature": "Mars/Jupiter", "effect": "Conflict, courage, sudden shifts."},
    {"name": "Aldebaran", "longitude": 70.0, "nature": "Mars", "effect": "Intelligence, eloquence, public honor."},
    {"name": "Sirius", "longitude": 104.0, "nature": "Jupiter/Mars", "effect": "Ambition, fame, high status."},
    {"name": "Algol", "longitude": 56.0, "nature": "Saturn/Mars", "effect": "Intensity, tragedy, or profound power if mastered."},
    {"name": "Vega", "longitude": 285.0, "nature": "Venus/Mercury", "effect": "Artistic talent, charisma, and public appeal."},
    {"name": "Arcturus", "longitude": 204.0, "nature": "Mars/Jupiter", "effect": "Success through determination and self-discovery."},
    {"name": "Fomalhaut", "longitude": 334.0, "nature": "Venus/Mercury", "effect": "Spiritual leadership, mysticism, or fame if idealistic."},
    {"name": "Deneb", "longitude": 325.0, "nature": "Venus/Mercury", "effect": "Intellectual power and quick success."},
    {"name": "Rigel", "longitude": 77.0, "nature": "Jupiter/Mars", "effect": "Success, wealth, and technical skill."},
    {"name": "Betelgeuse", "longitude": 89.0, "nature": "Mars/Mercury", "effect": "War-like success, or quick-witted dominance."},
    {"name": "Pollux", "longitude": 113.0, "nature": "Mars", "effect": "Protection, courage, but potential for rashness."},
    {"name": "Castor", "longitude": 110.0, "nature": "Mercury", "effect": "Intellectual talent, writing, and sharp mind."},
    {"name": "Sirius", "longitude": 104.0, "nature": "Jupiter/Mars", "effect": "Ambition, fame, high status."},
    {"name": "Canopus", "longitude": 105.0, "nature": "Saturn/Jupiter", "effect": "Wisdom, travel, and far-reaching influence."},
    {"name": "Alphard", "longitude": 147.0, "nature": "Saturn/Venus", "effect": "Intensity, depth, and creative passion."},
    {"name": "Bellatrix", "longitude": 81.0, "nature": "Mars/Mercury", "effect": "Swift success, courage, but potential for combativeness."},
    {"name": "Alnilam", "longitude": 83.0, "nature": "Jupiter/Saturn", "effect": "Public honor, fleeting fame, and organizational skill."},
    {"name": "Acrux", "longitude": 212.0, "nature": "Jupiter", "effect": "Spiritual power, mystery, and deep intuition."},
    {"name": "Spica", "longitude": 204.0, "nature": "Venus/Mars", "effect": "Fortune, wealth, artistic success."}
]

def analyze_fixed_star_conjunctions(planets: Dict[str, Any], ayanamsa: float) -> List[Dict[str, Any]]:
    """
    Check if any planet is conjunct a major fixed star.
    Uses an orb of 1 degree.
    """
    results = []

    for p_name, p_info in planets.items():
        if p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            # Sidereal Longitude of Planet
            p_lon = getattr(p_info, "longitude", 0)
            # We need to compare with Sidereal Star longitudes
            # For 2026, Regulus is ~0.5 deg Virgo Tropical.
            # If Lahiri Ayanamsa is ~24 deg, Sidereal Regulus is ~6 deg Leo.

            for star in FIXED_STARS:
                # Approximate sidereal conversion (Subtracting ayanamsa)
                sidereal_star_lon = (star["longitude"] - ayanamsa + 360) % 360

                if abs(p_lon - sidereal_star_lon) < 1.0:
                    results.append({
                        "planet": p_name,
                        "star": star["name"],
                        "nature": star["nature"],
                        "interpretation": f"{p_name} is conjunct Fixed Star {star['name']}: {star['effect']}"
                    })

    return results
