# Jyotish Dashboard 2.0 Engine
import os
import swisseph as swe

# Initialize ephemeris path globally for the package
# First check environment variable, then local 'ephe' folder
EPHE_PATH = os.getenv("SE_EPHE_PATH")
if not EPHE_PATH:
    # Try common local paths
    local_ephe = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ephe")
    if os.path.exists(local_ephe):
        EPHE_PATH = local_ephe

if EPHE_PATH:
    swe.set_ephe_path(EPHE_PATH)
    print(f"DEBUG: Swiss Ephemeris path set to: {EPHE_PATH}")
else:
    print("DEBUG: Swiss Ephemeris path NOT set. Calculations may be less accurate.")
