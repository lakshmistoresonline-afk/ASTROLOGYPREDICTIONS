# Centralized Swiss Ephemeris Proxy to handle missing dependency gracefully.
try:
    import swisseph as swe
except ImportError:
    swe = None

if not swe:
    # Minimal mock to prevent crash on attribute access during module loading
    class MockSWE:
        def __init__(self):
            # Define common constants
            self.SUN = 0
            self.MOON = 1
            self.MERCURY = 2
            self.VENUS = 3
            self.MARS = 4
            self.JUPITER = 5
            self.SATURN = 6
            self.URANUS = 7
            self.NEPTUNE = 8
            self.PLUTO = 9
            self.MEAN_NODE = 10
            self.TRUE_NODE = 11

            self.FLG_SWIEPH = 2
            self.FLG_SIDEREAL = 64
            self.FLG_SPEED = 256
            self.FLG_TOPOCTR = 32768

            self.SIDM_LAHIRI = 1
            self.SIDM_RAMAN = 0
            self.SIDM_KRISHNAMURTI = 5

        def __getattr__(self, name):
            # Return 0 for any other flags or IDs
            if name.startswith('FLG_') or name.startswith('SIDM_') or name.isupper():
                return 0
            # Return a dummy function for missing methods
            return lambda *args, **kwargs: None

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
            # h is decimal hour
            day_fraction = h / 24.0
            jd = int(365.25 * (y + 4716)) + int(30.6001 * (month + 1)) + d + day_fraction + b - 1524.5
            return jd

        def calc_ut(self, jd, pid, flags=0):
            # Planet Speeds (Approx Deg per Day)
            speeds = {0: 1.0, 1: 13.0, 2: 1.5, 3: 1.2, 4: 0.5, 5: 0.08, 6: 0.03, 7: 0.01, 8: 0.005, 9: 0.004, 10: -0.05, 11: -0.05}
            v = speeds.get(pid, 1.0)
            # Offset by JD 2451545.0 (J2000)
            diff = jd - 2451545.0
            mock_lon = ((pid + 1) * 40.5 + (diff * v)) % 360
            return ([mock_lon, 0.0, 1.0, v, 0.0, 0.0], 0)

        def get_ayanamsa_ut(self, jd): return 24.0 # Lahiri approx
        def sidtime(self, jd): return 0.0

        def houses_ex(self, jd, lat, lon, hsys, flags):
            # Return plausible house cusps (30 deg each)
            # Ascendant approx 0 for mock
            cusps = [0.0] + [ (i * 30.0) % 360 for i in range(12) ]
            ascmc = [0.0, 90.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            return (cusps + [0.0], ascmc)

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

            if year < 1: year = 1

            hour = (day - int(day)) * 24
            if hour >= 24: hour = 23.99
            return (year, month, int(day), hour)

        def sol_eclipse_when_next(self, jd, flags): return (0, [jd+30.0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        def lun_eclipse_when_next(self, jd, flags): return (0, [jd+15.0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    swe = MockSWE()
