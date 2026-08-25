# Centralized Swiss Ephemeris Proxy to handle missing dependency gracefully.
try:
    import swisseph as swe
except ImportError:
    swe = None

if not swe:
    # Minimal mock to prevent crash on attribute access during module loading
    class MockSWE:
        def __getattr__(self, name):
            # Return 0 for common flags and ids, or None for functions
            if name.startswith('FLG_') or name.startswith('SIDM_') or name.isupper():
                return 0
            return None

        def set_ephe_path(self, path): pass
        def set_sid_mode(self, mode): pass
        def set_topo(self, lon, lat, alt): pass
        def julday(self, y, m, d, h):
            # Standard Gregorian to JD fallback
            if m <= 2:
                y -= 1
                month = m + 12
            else:
                month = m
            a = int(y / 100)
            b = 2 - a + int(a / 4)
            jd = int(365.25 * (y + 4716)) + int(30.6001 * (month + 1)) + d + h / 24.0 + b - 1524.5
            return jd
        def calc_ut(self, jd, pid, flags=0):
            # Fallback for Sun and Moon using ephem if pid matches
            try:
                import ephem
                from .datetime import jd_to_datetime
                dt = jd_to_datetime(jd)
                obs = ephem.Observer()
                obs.date = dt

                body = ephem.Sun() if pid == 0 else ephem.Moon() if pid == 1 else None
                if body:
                    body.compute(obs)
                    ecl = ephem.Ecliptic(body)
                    import math
                    lon = float(ecl.lon) * 180 / math.pi
                    return ([lon, 0.0, 1.0, 1.0, 0.0, 0.0], 0)
            except Exception:
                pass
            return ([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 0)
        def get_ayanamsa_ut(self, jd): return 0.0
        def sidtime(self, jd): return 0.0
        def houses_ex(self, jd, lat, lon, hsys, flags): return ([0.0]*13, [0.0]*10)
        def revjul(self, jd):
            # Standard JD to Gregorian fallback
            z = int(jd + 0.5)
            f = jd + 0.5 - z
            if z < 2299161:
                a = z
            else:
                alpha = int((z - 1867216.25) / 36524.25)
                a = z + 1 + alpha - int(alpha / 4)
            b = a + 1524
            c = int((b - 122.1) / 365.25)
            d = int(365.25 * c)
            e = int((b - d) / 30.6001)
            day = b - d - int(30.6001 * e) + f
            month = e - 1 if e < 14 else e - 13
            year = c - 4716 if month > 2 else c - 4715

            # Python datetime safety: year must be >= 1
            if year < 1: year = 1

            hour = (day - int(day)) * 24
            return (year, month, int(day), hour)
        def sol_eclipse_when_next(self, jd, flags): return (0, [0.0]*10)
        def lun_eclipse_when_next(self, jd, flags): return (0, [0.0]*10)
        def rise_trans(self, *args): return (0, [0.0]*10)

    swe = MockSWE()
