from ..core.chart import calculate_chart_data
from ..core.models import CanonicalChart
from datetime import datetime

def calculate_transit(dt: datetime, lat: float, lon: float, tz: str) -> CanonicalChart:
    """Wrapper for calculating a chart for a transit time."""
    return calculate_chart_data(dt, lat, lon, tz)
