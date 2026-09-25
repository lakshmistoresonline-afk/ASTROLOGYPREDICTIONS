import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.store import save_chart
from app.utils.pdf_generator import generate_complete_pdf

def test_pdf_generation():
    print("================================================================================")
    print("📄 TESTING CANONICAL PDF REPORT GENERATION FROM REAL CHART DATA")
    print("================================================================================")

    app = create_app()
    with app.app_context():
        # Calculate real chart
        birth_dt = datetime(1986, 9, 28, 16, 30)
        chart_obj = calculate_canonical_chart(birth_dt, 10.7867, 76.6548, "Asia/Kolkata")

        data = {
            "profile": {
                "name": "Subramanian T S",
                "dob": "1986-09-28",
                "tob": "16:30",
                "place": "Palakkad, Kerala, India",
                "lat": 10.7867,
                "lon": 76.6548,
                "tz": "Asia/Kolkata"
            },
            "present": {
                "as_of": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "top_signals": [],
                "predictions": [],
                "timeline": []
            },
            "lifecycle": {"events": [], "phases": []},
            "clusters": [],
            "past_validation": [],
            "accuracy": {"real_world": {}, "historical": {}, "calibration": {}},
            "dashas": [],
            "metadata": {
                "engine": "V3.36 Authoritative",
                "calculation": "CALC-SWE-2.10.3",
                "ayanamsa": "Lahiri",
                "baseline_precision": "60.7%",
                "baseline_recall": "43.6%"
            }
        }

        # Generate PDF bytes
        pdf_bytes = generate_complete_pdf(data)
        assert pdf_bytes is not None
        assert len(pdf_bytes) > 1000

        print(f"  ✅ PDF Generated Successfully! Size: {len(pdf_bytes)} bytes")
        print("================================================================================")
        return True

if __name__ == "__main__":
    test_pdf_generation()
