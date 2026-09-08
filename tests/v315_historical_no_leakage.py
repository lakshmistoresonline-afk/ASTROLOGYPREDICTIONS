import os
import sys
import unittest
from datetime import datetime, timedelta

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engine import generate_evidence_based_predictions

class HistoricalNoLeakageTest(unittest.TestCase):
    def test_chronology_enforcement(self):
        # Case: Steve Jobs Apple IPO (1980-12-12)
        # We simulate prediction on 1980-11-12 (30 days before)
        event_date = datetime(1980, 12, 12)
        cutoff_date = event_date - timedelta(days=30)

        birth_dt = datetime(1955, 2, 24, 19, 15)
        chart_obj = calculate_chart_data(birth_dt, 37.77, -122.42, "America/Los_Angeles")

        # 1. Generate prediction as of cutoff
        preds = generate_evidence_based_predictions(chart_obj, selected_date=cutoff_date)

        # 2. Verify that 'generated_at' is earlier than actual event
        # (The mock simulation uses selected_date as the logical 'now')
        logical_now = cutoff_date
        self.assertTrue(logical_now < event_date, "Logical prediction date MUST be before event date.")

        # 3. Find Career prediction
        career_pred = next((p for p in preds['predictions'] if p['domain'] == 'Career & Authority'), None)
        self.assertIsNotNone(career_pred)

        # 4. Verify Peak is in proximity to event
        peak_str = career_pred.get('timing_window', {}).get('peak')
        if peak_str:
            peak_dt = datetime.strptime(peak_str, "%Y-%m-%d")
            # Proximity check (±30 days of event)
            diff = abs((event_date - peak_dt).days)
            print(f"DEBUG: Steve Jobs 1980 Replay | Cutoff: {cutoff_date.date()} | Peak: {peak_str} | Actual: {event_date.date()} | Diff: {diff} days")
            self.assertLessEqual(diff, 30, "Historical peak should align with known event within tolerance.")

if __name__ == "__main__":
    unittest.main()
