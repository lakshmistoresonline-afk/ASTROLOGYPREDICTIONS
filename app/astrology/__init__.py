# Jyotish Dashboard 2.0 Engine
import os
from .core.swe_proxy import swe

# Initialize ephemeris path globally if local 'swe' is available (for tests or local builds)
try:
    EPHE_PATH = os.getenv("SE_EPHE_PATH")
    if not EPHE_PATH:
        local_ephe = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ephe")
        if os.path.exists(local_ephe):
            EPHE_PATH = local_ephe

    if EPHE_PATH and hasattr(swe, 'set_ephe_path'):
        swe.set_ephe_path(EPHE_PATH)
except (ImportError, AttributeError):
    pass
