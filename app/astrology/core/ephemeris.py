from .swe_proxy import swe
import os
from typing import Dict, Any
from functools import lru_cache

# Force Sidereal Lahiri Ayanamsa as the project standard
EPHE_PATH = os.getenv("SE_EPHE_PATH", os.path.join(os.getcwd(), "ephe"))

def _init_swe():
    if hasattr(swe, 'set_ephe_path'):
        if os.path.exists(EPHE_PATH):
            try: swe.set_ephe_path(EPHE_PATH)
            except: pass
        try: swe.set_sid_mode(swe.SIDM_LAHIRI)
        except: pass

# Global configuration for topocentric precision
_USE_TOPO = True

def set_topocentric(lat: float, lon: float, alt: float = 0.0):
    if hasattr(swe, 'set_topo'):
        try: swe.set_topo(lon, lat, alt)
        except: pass

@lru_cache(maxsize=2048)
def get_planet_position(jd_ut: float, planet_id: int) -> Dict[str, Any]:
    # FLG_SIDEREAL | FLG_SPEED | FLG_TOPOCTR
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED | swe.FLG_TOPOCTR
    res, ret_flag = swe.calc_ut(jd_ut, planet_id, flags)
    return {
        "longitude": res[0], "latitude": res[1], "distance": res[2],
        "speed_long": res[3], "speed_lat": res[4], "speed_dist": res[5],
        "is_retrograde": res[3] < 0
    }

def get_ayanamsa(jd_ut: float) -> float:
    return swe.get_ayanamsa_ut(jd_ut)

# Initialize on import if possible
_init_swe()
