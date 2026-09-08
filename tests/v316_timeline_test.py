import os
import sys
from datetime import datetime, timedelta
import unittest

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.v316_timeline import lifetime_timeline_engine

class TimelineEngineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["FLASK_SECRET_KEY"] = "timeline-test-key"
        cls.app = create_app()

    def test_timeline_generation(self):
        with self.app.app_context():
            # Steve Jobs Case
            birth_dt = datetime(1955, 2, 24, 19, 15)
            lat, lon, tz = 37.77, -122.42, "America/Los_Angeles"
            chart_obj = calculate_chart_data(birth_dt, lat, lon, tz)

            print("\n[TEST] Generating V3.16 Lifetime Timeline...")
            # Generate shorter timeline for test speed (up to age 10)
            timeline = lifetime_timeline_engine.generate_lifetime_timeline(chart_obj, "test-jobs", end_age=10)

            self.assertGreater(len(timeline.events), 0)
            print(f"✅ Generated {len(timeline.events)} life events.")

            # Verify chronological order
            dates = [e.peak_date for e in timeline.events]
            self.assertEqual(dates, sorted(dates))
            print("✅ Events are strictly chronological.")

            # Verify age mapping
            for e in timeline.events[:5]:
                self.assertGreaterEqual(e.age_at_peak, 0)
                self.assertLessEqual(e.age_at_peak, 45)

            # Check phase summary
            phases = lifetime_timeline_engine.get_life_phase_summary(timeline)
            self.assertGreater(len(phases), 0)
            print(f"✅ Generated {len(phases)} life phase chapters.")

if __name__ == "__main__":
    unittest.main()
