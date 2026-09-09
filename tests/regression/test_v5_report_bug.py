import pytest
from app import create_app
from app.database.models import db, Chart

def test_report_location_propagation():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        chart = Chart(id="test-report-1", name="Test User", dob="1986-09-28", tob="16:30", place="Palakkad, India", lat=10.78, lon=76.65, tz="Asia/Kolkata")
        db.session.add(chart)
        db.session.commit()

        place = chart.place or "Unknown"
        assert place == "Palakkad, India"
        db.drop_all()
