"""
Stationing & Eclipse Micro-Transit Overlay Engine (Module 21 - Task 21.2).
Calculates exact astronomical stations (speed < 0.01 deg/day) and Solar/Lunar Eclipse points,
applying tight orb collision detection (<= 1.5 deg) against natal KP Sub-Lords and Dasha Lords.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

class StationingEclipseTracker:
    """
    Detects planetary stations (speed approx 0 deg/day) and Solar/Lunar Eclipse collisions (<= 1.5 deg).
    """

    @staticmethod
    def detect_planetary_stations(
        daily_transits: Dict[str, Dict[str, float]]
    ) -> List[Dict[str, Any]]:
        """
        Detects planets with daily speed < 0.01 deg/day (Stationary Direct or Stationary Retrograde).
        """
        stations = []
        for p_name, t_data in daily_transits.items():
            speed = abs(t_data.get("speed", 1.0))
            if speed <= 0.01:
                stations.append({
                    "planet": p_name,
                    "longitude": round(t_data.get("lon", 0.0), 2),
                    "daily_speed": round(speed, 4),
                    "station_type": "STATIONARY_DIRECT" if t_data.get("speed", 0.0) >= 0 else "STATIONARY_RETROGRADE",
                    "impact_level": "HIGH_IMPACT_TRANSIT_STATION"
                })
        return stations

    @staticmethod
    def detect_eclipse_collisions(
        eclipse_longitudes: List[float],
        natal_points: Dict[str, float],
        orb_tolerance: float = 1.5
    ) -> List[Dict[str, Any]]:
        """
        Collision detection between Solar/Lunar Eclipse points and natal KP Sub-Lords / Dasha Lords within <= 1.5 deg.
        """
        collisions = []
        for e_lon in eclipse_longitudes:
            for n_name, n_lon in natal_points.items():
                diff = abs(e_lon - n_lon) % 360.0
                if diff > 180.0: diff = 360.0 - diff

                if diff <= orb_tolerance:
                    collisions.append({
                        "natal_point": n_name,
                        "natal_longitude": round(n_lon, 2),
                        "eclipse_longitude": round(e_lon, 2),
                        "orb_difference": round(diff, 2),
                        "trigger_type": "ECLIPSE_NATAL_COLLISION",
                        "risk_opportunity_rating": "HIGH_VOLATILITY_TRANSITION"
                    })

        return collisions

stationing_eclipse_tracker = StationingEclipseTracker()
