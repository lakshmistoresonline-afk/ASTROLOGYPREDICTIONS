import os
import sys
import pytest

sys.path.append('D:/ASTROLOGYPREDICTIONS')

from app import create_app
from app.astrology.predictions.engine import generate_evidence_based_predictions
from app.routes import _load_active_chart
from flask import session

app = create_app()

@pytest.mark.parametrize("pid", ["de9427a1"])
def test_profile(pid):
    with app.test_request_context():
        session['active_chart_id'] = pid
        chart_data, chart_obj = _load_active_chart()
        if chart_obj:
            preds = generate_evidence_based_predictions(chart_obj)
            assert preds is not None
            assert 'predictions' in preds
