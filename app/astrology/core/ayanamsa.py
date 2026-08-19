import swisseph as swe

# Common Ayanamsa constants
AYANAMSA_MODES = {
    "LAHIRI": swe.SIDM_LAHIRI,
    "RAMAN": swe.SIDM_RAMAN,
    "KP": swe.SIDM_KRISHNAMURTI,
    "FAGAN_BRADLEY": swe.SIDM_FAGAN_BRADLEY,
    "J_BHASIN": swe.SIDM_JN_BHASIN,
}

def set_ayanamsa_mode(mode: str = "LAHIRI"):
    """Set the sidereal mode for Swiss Ephemeris."""
    swe_mode = AYANAMSA_MODES.get(mode.upper(), swe.SIDM_LAHIRI)
    swe.set_sid_mode(swe_mode)

def get_current_ayanamsa(jd_ut: float) -> float:
    """Return the value of ayanamsa for a given JD."""
    return swe.get_ayanamsa_ut(jd_ut)
