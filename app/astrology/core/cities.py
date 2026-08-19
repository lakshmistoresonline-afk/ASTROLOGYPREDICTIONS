# High-Density Local City Database (Apotheosis Mode)
# This allows 100% offline geocoding for major global hubs.

OFFLINE_CITIES = [
    {"name": "New Delhi", "lat": 28.6139, "lon": 77.2090, "tz": "Asia/Kolkata", "country": "India"},
    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777, "tz": "Asia/Kolkata", "country": "India"},
    {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946, "tz": "Asia/Kolkata", "country": "India"},
    {"name": "London", "lat": 51.5074, "lon": -0.1278, "tz": "Europe/London", "country": "UK"},
    {"name": "New York", "lat": 40.7128, "lon": -74.0060, "tz": "America/New_York", "country": "USA"},
    {"name": "Dubai", "lat": 25.2048, "lon": 55.2708, "tz": "Asia/Dubai", "country": "UAE"},
    {"name": "Singapore", "lat": 1.3521, "lon": 103.8198, "tz": "Asia/Singapore", "country": "Singapore"},
    {"name": "Sydney", "lat": -33.8688, "lon": 151.2093, "tz": "Australia/Sydney", "country": "Australia"},
    {"name": "Toronto", "lat": 43.6532, "lon": -79.3832, "tz": "America/Toronto", "country": "Canada"},
    {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503, "tz": "Asia/Tokyo", "country": "Japan"},
    {"name": "Paris", "lat": 48.8566, "lon": 2.3522, "tz": "Europe/Paris", "country": "France"},
    {"name": "Chennai", "lat": 13.0827, "lon": 80.2707, "tz": "Asia/Kolkata", "country": "India"},
    {"name": "Hyderabad", "lat": 17.3850, "lon": 78.4867, "tz": "Asia/Kolkata", "country": "India"},
    {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639, "tz": "Asia/Kolkata", "country": "India"},
    # [A full database would contain 150,000 cities, this is the core hub subset]
]

def search_offline_city(query: str):
    query = query.lower()
    results = []
    for city in OFFLINE_CITIES:
        if query in city["name"].lower() or query in city["country"].lower():
            results.append({
                "display_name": f"{city['name']}, {city['country']} (Offline)",
                "lat": city["lat"],
                "lon": city["lon"],
                "timezone": city["tz"]
            })
    return results
