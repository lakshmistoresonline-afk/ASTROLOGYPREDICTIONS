# Jyotish Dashboard 2.0 Engine
import os
from .core.swe_proxy import swe

# Initialize ephemeris path globally for the package
EPHE_PATH = os.getenv("SE_EPHE_PATH")
if not EPHE_PATH:
    local_ephe = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ephe")
    if os.path.exists(local_ephe):
        EPHE_PATH = local_ephe

if swe and EPHE_PATH:
    swe.set_ephe_path(EPHE_PATH)
elif not swe:
    print("⚠ WARNING: 'pyswisseph' module not found. Calculations will be mocked.")
