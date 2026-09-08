import os
import sys

# Set up path
sys.path.append('D:/ASTROLOGYPREDICTIONS')

from app import create_app
from app.astrology.predictions.engine import generate_evidence_based_predictions
from app.routes import _load_active_chart
from flask import session

app = create_app()

def test_profile(pid):
    with app.test_request_context():
        session['active_chart_id'] = pid
        chart_data, chart_obj = _load_active_chart()
        if not chart_obj:
            print(f"Failed to load {pid}")
            return

        print(f"Profile: {chart_data['name']}")
        preds = generate_evidence_based_predictions(chart_obj)
        top = preds['predictions'][0]
        print(f"Top Domain: {top['domain']}")
        print(f"Top Score: {top['score']}")
        print(f"Top Event: {top['event_type']}")
        print("-" * 20)

print("Checking Profile A (de9427a1)...")
test_profile('de9427a1')

print("Checking Profile B (913637d9)...")
test_profile('913637d9')
