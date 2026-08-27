from .swe_proxy import swe
from datetime import datetime
from typing import List, Dict, Any

def get_upcoming_eclipses(jd_start: float, count: int = 5) -> List[Dict[str, Any]]:
    """Find the next N solar and lunar eclipses."""
    results = []
    curr_jd = jd_start

    from .datetime import jd_to_datetime
    for _ in range(count):
        # 1. Solar Eclipse
        res = swe.sol_eclipse_when_next(curr_jd, swe.FLG_SWIEPH)
        jd_solar = res[1][0]
        results.append({
            "type": "Solar Eclipse",
            "jd": jd_solar,
            "date": jd_to_datetime(jd_solar).isoformat(),
            "longitude": swe.calc_ut(jd_solar, swe.SUN)[0][0]
        })

        # 2. Lunar Eclipse
        res_l = swe.lun_eclipse_when_next(curr_jd, swe.FLG_SWIEPH)
        jd_lunar = res_l[1][0]
        results.append({
            "type": "Lunar Eclipse",
            "jd": jd_lunar,
            "date": jd_to_datetime(jd_lunar).isoformat(),
            "longitude": swe.calc_ut(jd_lunar, swe.MOON)[0][0]
        })

        curr_jd = max(jd_solar, jd_lunar) + 1.0

    return sorted(results, key=lambda x: x["jd"])

def check_eclipse_impact(chart_planets: Dict[str, Any], eclipses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Check if any eclipse falls near natal planets (Orb 2 deg)."""
    impacts = []
    for ec in eclipses:
        ec_lon = ec["longitude"]
        for p_name, p_info in chart_planets.items():
            p_lon = getattr(p_info, "longitude", 0)
            diff = abs(p_lon - ec_lon) % 360
            if diff > 180: diff = 360 - diff

            if diff < 2.0:
                impacts.append({
                    "eclipse": ec["type"],
                    "date": ec["date"],
                    "planet": p_name,
                    "interpretation": f"The {ec['type']} on {ec['date']} falls exactly on your natal {p_name}, suggesting a major transformation in that area of life."
                })
    return impacts
