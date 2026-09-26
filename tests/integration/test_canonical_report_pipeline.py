import pytest
import os
from datetime import datetime
from app import create_app
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.reporting.builder import build_canonical_astrology_report
from app.astrology.reporting.validators import validate_canonical_report
from app.astrology.reporting.models import ReportBuildError
from app.utils.pdf_generator import generate_complete_pdf

def test_d10_independent_derivation():
    """Verifies that D10 Dashamsha placements are calculated independently from D1 Rashi."""
    birth_dt = datetime(1986, 9, 28, 16, 30)
    chart_obj = calculate_canonical_chart(birth_dt, 10.7867, 76.6548, "Asia/Kolkata")
    report = build_canonical_astrology_report(chart_obj, selected_date=datetime.now())

    differing_vargas = 0
    print("\n-------------------------------------------------------------")
    print("Planet | D1 (Rashi) | D9 (Navamsha) | D10 (Dashamsha)")
    print("-------------------------------------------------------------")
    for v in report.varga_placements:
        print(f"{v.planet:7s} | {v.d1_sign:10s} | {v.d9_sign:12s} | {v.d10_sign:13s}")
        if v.d1_sign != v.d10_sign:
            differing_vargas += 1
    print("-------------------------------------------------------------")

    assert len(report.varga_placements) >= 9
    assert differing_vargas >= 1, "D10 Dashamsha must be independently derived and differ from D1 Rashi!"

def test_report_builder_missing_mandatory_data_raises_error():
    """Verifies that building a report with missing mandatory chart data raises ReportBuildError."""
    with pytest.raises(ReportBuildError):
        build_canonical_astrology_report(None)

def test_authenticated_report_download_route():
    """Verifies the HTTP GET /report/download route produces real PDF report."""
    app = create_app()
    client = app.test_client()

    # Save a chart profile and set authenticated session
    from app.astrology.store import save_chart
    with app.app_context():
        chart_data = {
            "name": "Subramanian T S Test Native",
            "birth_dob": "1986-09-28",
            "birth_tob": "16:30",
            "birth_place": "Palakkad, Kerala, India",
            "latitude": 10.7867,
            "longitude": 76.6548,
            "timezone": "Asia/Kolkata"
        }
        cid = save_chart("uid_tester", chart_data)

    with client.session_transaction() as sess:
        sess["firebase_id_token"] = "mock_token_admin"
        sess["firebase_uid"] = "uid_tester"
        sess["birth_name"] = "Subramanian T S Test Native"
        sess["birth_dob"] = "1986-09-28"
        sess["birth_tob"] = "16:30"
        sess["birth_place"] = "Palakkad, Kerala, India"
        sess["birth_lat"] = 10.7867
        sess["birth_lon"] = 76.6548
        sess["birth_tz"] = "Asia/Kolkata"
        sess["active_chart_id"] = cid

    # Request HTTP GET /report/download
    res = client.get("/report/download")
    assert res.status_code == 200
    assert "application/pdf" in res.headers["Content-Type"]

    pdf_bytes = res.get_data()
    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 2000

    try:
        import io
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text() or ""
        assert "ASTRO PREDICTIONS" in pdf_text
        assert "Steve Jobs" not in pdf_text
        assert "Mahatma Gandhi" not in pdf_text
    except ImportError:
        assert len(pdf_bytes) > 2000

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
        pdf_bytes = generate_complete_pdf(report.to_dict())
        assert pdf_bytes is not None
        assert len(pdf_bytes) > 2000
        assert pdf_bytes.startswith(b"%PDF")

        # 6. Verify zero historical demo names appear in native report
        try:
            import io
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(pdf_bytes))
            pdf_text = ""
            for page in reader.pages:
                pdf_text += page.extract_text() or ""
            assert "ASTRO PREDICTIONS" in pdf_text
            assert "Steve Jobs" not in pdf_text
            assert "Mahatma Gandhi" not in pdf_text
        except ImportError:
            assert len(pdf_bytes) > 2000
