# Centralized Swiss Ephemeris Proxy.
# Enforces deterministic calculations by requiring swisseph for functions.
import sys
import os

try:
    import swisseph as swe
except ImportError:
    # Diagnostic: check for venv presence
    venv_site = os.path.join(os.getcwd(), "venv", "Lib", "site-packages")
    if os.path.exists(venv_site) and venv_site not in sys.path:
        sys.path.append(venv_site)
        try:
            import swisseph as swe
        except ImportError:
            swe = None
    else:
        swe = None

if not swe:
    class ProxyError:
        SUN = 0
        MOON = 1
        MERCURY = 2
        VENUS = 3
        MARS = 4
        JUPITER = 5
        SATURN = 6
        URANUS = 7
        NEPTUNE = 8
        PLUTO = 9
        MEAN_NODE = 10
        TRUE_NODE = 11

        SIDM_LAHIRI = 1
        FLG_SIDEREAL = 64
        FLG_SPEED = 256
        FLG_TOPOCTR = 32768

        def __getattr__(self, name):
            # Allow hasattr() to return False for non-existent methods
            if name in ['__wrapped__', '__members__', '__methods__', '__class__']:
                raise AttributeError(name)

            def _fail(*args, **kwargs):
                raise ImportError(
                    f"Swiss Ephemeris function '{name}' called but pyswisseph is not installed. "
                    "Please ensure the Calculation Service is running or install pyswisseph locally."
                )
            return _fail

    swe = ProxyError()
