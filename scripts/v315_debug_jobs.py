import os
import sys
from datetime import datetime, timedelta

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engines.career import CareerPredictionEngine

def main():
    os.environ["FLASK_SECRET_KEY"] = "debug-key"
    app = create_app()

    # Steve Jobs: 1955-02-24
    birth_dt = datetime(1955, 2, 24, 19, 15)
    chart = calculate_chart_data(birth_dt, 37.77, -122.42, "America/Los_Angeles")

    # Event: IPO 1980-12-12
    sim_date = datetime(1980, 11, 12)

    with app.app_context():
        print(f"Jobs Chart Details:")
        print(f"  Ascendant: {chart.ascendant:.2f} ({chart.asc_rashi+1} Rashi)")
        for p_name, p in chart.planets.items():
            print(f"  {p_name:10} : House {p.house} ({p.longitude:.2f} deg)")

        pred = CareerPredictionEngine.get_prediction(chart, sim_date)
        print(f"Jobs Career 1980:")
        print(f"  Strength: {pred.prediction_strength}")
        print(f"  Score: {pred.score}")
        print(f"  Q: {pred.quality_score}")
        print(f"  Timing: {pred.timing_window.get('phase')} ({pred.timing_window.get('proximity_weight'):.2f})")

if __name__ == "__main__":
    main()
