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
        def julday(self, y, m, d, h): return 0.0
        def calc_ut(self, jd, pid, flags=0): return ([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 0)
        def get_ayanamsa_ut(self, jd): return 0.0
        def sidtime(self, jd): return 0.0
        def houses_ex(self, jd, lat, lon, hsys, flags): return ([0.0]*13, [0.0]*10)
        def revjul(self, jd): return (2000, 1, 1, 12.0)
        def sol_eclipse_when_next(self, jd, flags): return (0, [0.0]*10)
        def lun_eclipse_when_next(self, jd, flags): return (0, [0.0]*10)
        def rise_trans(self, *args): return (0, [0.0]*10)

    swe = MockSWE()
