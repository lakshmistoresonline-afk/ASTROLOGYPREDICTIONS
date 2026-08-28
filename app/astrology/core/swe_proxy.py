# Centralized Swiss Ephemeris Proxy.
# Enforces deterministic calculations by requiring swisseph for functions.
try:
    import swisseph as swe
except ImportError:
    swe = None

if not swe:
    class ProxyError:
        # Standard IDs to avoid module-level import errors
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
            # Fail loudly only when a function is called
            def _fail(*args, **kwargs):
                raise ImportError(
                    f"Swiss Ephemeris function '{name}' called but pyswisseph is not installed. "
                    "Please ensure the Calculation Service is running or install pyswisseph locally."
                )
            return _fail

    swe = ProxyError()
