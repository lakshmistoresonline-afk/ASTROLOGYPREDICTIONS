"""
Geo-Spatial Transit Mapping & AstroCartoGraphy Engine (V8.0 - Part 2).
Computes geographic coordinates where planets are on Ascendant (Asc), Midheaven (MC),
Descendant (Dsc), or Nadir (IC), outputting GeoJSON vector paths for interactive map overlays.
"""
from typing import Dict, Any, List

class AstroCartoGraphyEngine:
    """
    Computes planetary Zenith, Midheaven (MC), Nadir (IC), Ascendant, and Descendant lines across Earth coordinates.
    """

    @staticmethod
    def generate_planetary_lines_geojson(planets: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates GeoJSON FeatureCollection containing line strings for planetary MC and IC meridian lines.
        """
        features = []

        for p_name, p_info in planets.items():
            lon_p = getattr(p_info, "longitude", p_info if isinstance(p_info, (int, float)) else 0.0)

            # Calculate Midheaven (MC) longitude line (-180 to +180 deg)
            mc_lon = (lon_p - 180.0) % 360.0 - 180.0
            ic_lon = (lon_p) % 360.0 - 180.0

            # MC Meridian Line (North Pole to South Pole at mc_lon)
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[mc_lon, 85.0], [mc_lon, -85.0]]
                },
                "properties": {
                    "planet": p_name,
                    "line_type": "MC",
                    "description": f"{p_name} Midheaven (MC) Line — High Career & Public Visibility Zone"
                }
            })

            # IC Meridian Line (North Pole to South Pole at ic_lon)
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[ic_lon, 85.0], [ic_lon, -85.0]]
                },
                "properties": {
                    "planet": p_name,
                    "line_type": "IC",
                    "description": f"{p_name} Nadir (IC) Line — Home, Family & Emotional Grounding Zone"
                }
            })

        return {
            "type": "FeatureCollection",
            "features": features
        }

    @staticmethod
    def evaluate_relocation_chart(
        chart_obj: Any,
        target_city: str,
        target_lat: float,
        target_lon: float
    ) -> Dict[str, Any]:
        """
        Evaluates planetary house shifts when moving to a new city/latitude/longitude.
        """
        from .core.high_latitude_cusps import high_latitude_cusp_engine

        jd_ut = chart_obj.birth_datetime.timestamp()
        relocated_houses = high_latitude_cusp_engine.calculate_houses_polar_safe(jd_ut, target_lat, target_lon)

        shifted_planets = []
        for p_name, p in getattr(chart_obj, "planets", {}).items():
            p_lon = p.longitude
            # Calculate house placement under new relocated ascendant
            rel_asc = relocated_houses["ascendant"]
            rel_house = (int((p_lon - rel_asc + 360.0) % 360.0 // 30)) + 1

            shifted_planets.append({
                "planet": p_name,
                "natal_house": p.house,
                "relocated_house": rel_house,
                "house_shifted": p.house != rel_house
            })

        return {
            "target_city": target_city,
            "target_coordinates": {"latitude": target_lat, "longitude": target_lon},
            "relocated_ascendant": round(relocated_houses["ascendant"], 2),
            "shifted_planets": shifted_planets
        }

astrocartography_engine = AstroCartoGraphyEngine()
