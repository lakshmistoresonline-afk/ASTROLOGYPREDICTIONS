from typing import List, Dict, Any, Optional

CANONICAL_LOCATIONS = [
    {
        "location_id": "geonames:1269750",
        "name": "New Delhi",
        "display_name": "New Delhi, Delhi, India",
        "country": "India",
        "country_code": "IN",
        "state": "Delhi",
        "district": "New Delhi",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": "Asia/Kolkata",
        "source": "OFFLINE_LOCATION_DB",
        "precision": "city"
    },
    {
        "location_id": "geonames:1275339",
        "name": "Mumbai",
        "display_name": "Mumbai, Maharashtra, India",
        "country": "India",
        "country_code": "IN",
        "state": "Maharashtra",
        "district": "Mumbai",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "timezone": "Asia/Kolkata",
        "source": "OFFLINE_LOCATION_DB",
        "precision": "city"
    },
    {
        "location_id": "geonames:1277333",
        "name": "Bangalore",
        "display_name": "Bangalore, Karnataka, India",
        "country": "India",
        "country_code": "IN",
        "state": "Karnataka",
        "district": "Bangalore Urban",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "timezone": "Asia/Kolkata",
        "source": "OFFLINE_LOCATION_DB",
        "precision": "city"
    },
    {
        "location_id": "geonames:2643743",
        "name": "London",
        "display_name": "London, England, United Kingdom",
        "country": "United Kingdom",
        "country_code": "GB",
        "state": "England",
        "district": "Greater London",
        "latitude": 51.5074,
        "longitude": -0.1278,
        "timezone": "Europe/London",
        "source": "OFFLINE_LOCATION_DB",
        "precision": "city"
    },
    {
        "location_id": "geonames:5128581",
        "name": "New York",
        "display_name": "New York, New York, United States",
        "country": "United States",
        "country_code": "US",
        "state": "New York",
        "district": "New York",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "timezone": "America/New_York",
        "source": "OFFLINE_LOCATION_DB",
        "precision": "city"
    },
    {
        "location_id": "geonames:292223",
        "name": "Dubai",
        "display_name": "Dubai, Dubai, United Arab Emirates",
        "country": "United Arab Emirates",
        "country_code": "AE",
        "state": "Dubai",
        "district": "Dubai",
        "latitude": 25.2048,
        "longitude": 55.2708,
        "timezone": "Asia/Dubai",
        "source": "OFFLINE_LOCATION_DB",
        "precision": "city"
    },
    {
        "location_id": "geonames:1880252",
        "name": "Singapore",
        "display_name": "Singapore, Singapore, Singapore",
        "country": "Singapore",
        "country_code": "SG",
        "state": "Singapore",
        "district": "Singapore",
        "latitude": 1.3521,
        "longitude": 103.8198,
        "timezone": "Asia/Singapore",
        "source": "OFFLINE_LOCATION_DB",
        "precision": "city"
    },
    {
        "location_id": "geonames:2147714",
        "name": "Sydney",
        "display_name": "Sydney, New South Wales, Australia",
        "country": "Australia",
        "country_code": "AU",
        "state": "New South Wales",
        "district": "Sydney",
        "latitude": -33.8688,
        "longitude": 151.2093,
        "timezone": "Australia/Sydney",
        "source": "OFFLINE_LOCATION_DB",
        "precision": "city"
    },
    {
        "location_id": "geonames:6167865",
        "name": "Toronto",
        "display_name": "Toronto, Ontario, Canada",
        "country": "Canada",
        "country_code": "CA",
        "state": "Ontario",
        "district": "Toronto",
        "latitude": 43.6532,
        "longitude": -79.3832,
        "timezone": "America/Toronto",
        "source": "OFFLINE_LOCATION_DB",
        "precision": "city"
    },
    {
        "location_id": "geonames:1850147",
        "name": "Tokyo",
        "display_name": "Tokyo, Tokyo, Japan",
        "country": "Japan",
        "country_code": "JP",
        "state": "Tokyo",
        "district": "Tokyo",
        "latitude": 35.6762,
        "longitude": 139.6503,
        "timezone": "Asia/Tokyo",
        "source": "OFFLINE_LOCATION_DB",
        "precision": "city"
    },
    {
        "location_id": "geonames:2968815",
        "name": "Paris",
        "display_name": "Paris, Ile-de-France, France",
        "country": "France",
        "country_code": "FR",
        "state": "Ile-de-France",
        "district": "Paris",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "timezone": "Europe/Paris",
        "source": "OFFLINE_LOCATION_DB",
        "precision": "city"
    },
    {
        "location_id": "geonames:1264418",
        "name": "Chennai",
        "display_name": "Chennai, Tamil Nadu, India",
        "country": "India",
        "country_code": "IN",
        "state": "Tamil Nadu",
        "district": "Chennai",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "timezone": "Asia/Kolkata",
        "source": "OFFLINE_LOCATION_DB",
        "precision": "city"
    },
    {
        "location_id": "geonames:1269843",
        "name": "Hyderabad",
        "display_name": "Hyderabad, Telangana, India",
        "country": "India",
        "country_code": "IN",
        "state": "Telangana",
        "district": "Hyderabad",
        "latitude": 17.3850,
        "longitude": 78.4867,
        "timezone": "Asia/Kolkata",
        "source": "OFFLINE_LOCATION_DB",
        "precision": "city"
    },
    {
        "location_id": "geonames:1275004",
        "name": "Kolkata",
        "display_name": "Kolkata, West Bengal, India",
        "country": "India",
        "country_code": "IN",
        "state": "West Bengal",
        "district": "Kolkata",
        "latitude": 22.5726,
        "longitude": 88.3639,
        "timezone": "Asia/Kolkata",
        "source": "OFFLINE_LOCATION_DB",
        "precision": "city"
    },
    {
        "location_id": "geonames:1273874",
        "name": "Coimbatore",
        "display_name": "Coimbatore, Tamil Nadu, India",
        "country": "India",
        "country_code": "IN",
        "state": "Tamil Nadu",
        "district": "Coimbatore",
        "latitude": 11.0168,
        "longitude": 76.9558,
        "timezone": "Asia/Kolkata",
        "source": "OFFLINE_LOCATION_DB",
        "precision": "city"
    },
    {
        "location_id": "geonames:1256237",
        "name": "Thrissur",
        "display_name": "Thrissur, Kerala, India",
        "country": "India",
        "country_code": "IN",
        "state": "Kerala",
        "district": "Thrissur",
        "latitude": 10.5276,
        "longitude": 76.2144,
        "timezone": "Asia/Kolkata",
        "source": "OFFLINE_LOCATION_DB",
        "precision": "city"
    },
    {
        "location_id": "geonames:1262332",
        "name": "Palakkad",
        "display_name": "Palakkad, Kerala, India",
        "country": "India",
        "country_code": "IN",
        "state": "Kerala",
        "district": "Palakkad",
        "latitude": 10.7867,
        "longitude": 76.6547,
        "timezone": "Asia/Kolkata",
        "source": "OFFLINE_LOCATION_DB",
        "precision": "city"
    }
]

def search_canonical_locations(query: str) -> List[Dict[str, Any]]:
    if not query:
        return []
    q = query.strip().lower()
    results = []
    for loc in CANONICAL_LOCATIONS:
        if q in loc["name"].lower() or q in loc["display_name"].lower() or q in loc["state"].lower():
            results.append(loc)
    return results

def get_location_by_id(location_id: str) -> Optional[Dict[str, Any]]:
    for loc in CANONICAL_LOCATIONS:
        if loc["location_id"] == location_id:
            return loc
    return None
