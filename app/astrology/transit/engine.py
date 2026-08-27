from ..core.chart import calculate_chart_data
from ..core.models import CanonicalChart
from datetime import datetime

def calculate_transit(dt: datetime, lat: float, lon: float, tz: str) -> CanonicalChart:
    """Wrapper for calculating a chart for a transit time. Floored to 15m to use cache."""
    # Floor to nearest 15 minutes to maximize cache hits in calculate_chart_data
    dt_floored = dt.replace(minute=(dt.minute // 15) * 15, second=0, microsecond=0)
    return calculate_chart_data(dt_floored, lat, lon, tz)
