# Jyotish Dashboard 2.0 Engine
import os

try:
    import swisseph as swe
    # Initialize ephemeris path globally for the package
    EPHE_PATH = os.getenv("SE_EPHE_PATH")
    if not EPHE_PATH:
        local_ephe = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ephe")
        if os.path.exists(local_ephe):
            EPHE_PATH = local_ephe

    if EPHE_PATH:
        swe.set_ephe_path(EPHE_PATH)
        # print(f"DEBUG: Swiss Ephemeris path set to: {EPHE_PATH}")
    else:
        print("⚠ WARNING: Swiss Ephemeris path NOT set. Calculations may be less accurate.")
except ImportError:
    print("❌ CRITICAL: 'pyswisseph' module not found.")
    print("Please run 'python scripts/doctor.py' to fix your environment.")
    swe = None
