import os
import sys
from datetime import datetime

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.astrology.core.chart import calculate_chart_data
from app.astrology.dasha import calculate_vimshottari

def main():
    # Tom Hanks: 1956-07-09
    birth_dt = datetime(1956, 7, 9, 11, 17)
    chart = calculate_chart_data(birth_dt, 37.83, -121.9, "America/Los_Angeles")
    sim_date = datetime(1994, 3, 21)
    moon_lon = chart.planets["Moon"].longitude
    dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=sim_date)
    print(f"Hanks 1994 Dasha: {dasha.get('current_maha', {}).get('lord')} / {dasha.get('current_antar', {}).get('lord')}")

if __name__ == "__main__":
    main()
