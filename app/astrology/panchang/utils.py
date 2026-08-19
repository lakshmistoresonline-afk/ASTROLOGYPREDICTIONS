from typing import Callable

def find_event(start_jd: float, end_jd: float, func: Callable[[float], float], target: float, tolerance: float = 1e-6) -> float:
    """
    Find the JD where func(jd) == target using bisection method.
    Assumes func is monotonic in the interval [start_jd, end_jd].
    """
    low = start_jd
    high = end_jd

    # Normalize angles if necessary
    def get_val(jd):
        val = func(jd)
        diff = (val - target + 180) % 360 - 180
        return diff

    v_low = get_val(low)
    v_high = get_val(high)

    if v_low * v_high > 0:
        # Not crossing target in this interval or not monotonic
        return -1.0

    for _ in range(50): # Max iterations
        mid = (low + high) / 2
        v_mid = get_val(mid)
        if abs(v_mid) < tolerance:
            return mid
        if v_low * v_mid < 0:
            high = mid
            v_high = v_mid
        else:
            low = mid
            v_low = v_mid
    return (low + high) / 2
