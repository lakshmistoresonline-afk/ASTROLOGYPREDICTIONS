import pytest
import os
from datetime import datetime
from app import create_app
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.reporting.builder import build_canonical_astrology_report
from app.astrology.reporting.validators import validate_canonical_report
from app.utils.pdf_generator import generate_complete_pdf

def test_canonical_astrology_report_pipeline_end_to_end():
    app = create_app()
    with app.app_context():
        # 1. Calculate real active chart
        birth_dt = datetime(1986, 9, 28, 16, 30)
        chart_obj = calculate_canonical_chart(birth_dt, 10.7867, 76.6548, "Asia/Kolkata")

        # 2. Build Canonical Report
        report = build_canonical_astrology_report(chart_obj, selected_date=datetime.now())
        assert report is not None
        assert report.report_id.startswith("rep_")

        # 3. Validate Report
        is_valid, errors = validate_canonical_report(report)
        assert is_valid is True, f"Report validation failed: {errors}"

        # 4. Verify Non-Empty Astrology Sections
        assert len(report.planets) >= 9 # Sun through Ketu
        assert len(report.house_cusps) == 12
        assert len(report.varga_placements) >= 9
        assert len(report.dashas) >= 5
        assert len(report.predictions) >= 4
        assert len(report.timeline) >= 2

        # 5. Render PDF Report
        report_dict = report.to_dict()
        pdf_payload = {
            "profile": report_dict["profile"],
            "present": {
                "as_of": report_dict["created_at"],
                "top_signals": [p for p in report_dict["predictions"] if p["prediction_strength"] in ["PEAK", "ACTIVE"]][:3],
                "predictions": report_dict["predictions"]
            },
            "lifecycle": {
                "events": report_dict["timeline"]
            },
            "dashas": report_dict["dashas"],
            "metadata": report_dict["provenance"]
        }

        pdf_bytes = generate_complete_pdf(pdf_payload)
        assert pdf_bytes is not None
        assert len(pdf_bytes) > 2000
        assert pdf_bytes.startswith(b"%PDF")

        # 6. Verify zero historical demo names appear in native report
        pdf_text = pdf_bytes.decode('latin-1', 'ignore')
        assert "Steve Jobs" not in pdf_text
