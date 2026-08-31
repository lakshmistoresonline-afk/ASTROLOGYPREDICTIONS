from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    charts = db.relationship('Chart', backref='profile', lazy=True, cascade="all, delete-orphan")

class Chart(db.Model):
    __tablename__ = 'charts'
    id = db.Column(db.String(36), primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=True)
    name = db.Column(db.String(100))
    dob = db.Column(db.String(20))
    tob = db.Column(db.String(10))
    place = db.Column(db.String(200))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    tz = db.Column(db.String(50))
    raw_data = db.Column(db.Text)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_data(self, data: dict):
        self.raw_data = json.dumps(data, default=str)

    def get_data(self) -> dict:
        return json.loads(self.raw_data) if self.raw_data else {}

class PredictionOutcome(db.Model):
    """
    Immutable Prediction Snapshot & Outcome Tracking (V1.0.0).
    Stores engine versions to ensure reproducibility.
    """
    __tablename__ = 'prediction_outcomes'
    id = db.Column(db.Integer, primary_key=True)
    chart_id = db.Column(db.String(36), db.ForeignKey('charts.id'), nullable=False)

    # Engine Versions
    calculation_version = db.Column(db.String(50))
    dasha_version = db.Column(db.String(50))
    transit_version = db.Column(db.String(50))
    evidence_version = db.Column(db.String(50))
    remedy_version = db.Column(db.String(50))
    prompt_version = db.Column(db.String(50))

    domain = db.Column(db.String(50), nullable=False)
    prediction_strength = db.Column(db.String(20))
    engine_confidence = db.Column(db.String(20))
    confluence_score = db.Column(db.Float) # V3 Calibration
    quality_score = db.Column(db.Float) # V3 Metric
    prediction_text = db.Column(db.Text, nullable=False)

    # Point-in-Time Simulation (V3.1)
    historical_prediction_date = db.Column(db.DateTime, nullable=True)

    # Timing Snapshot
    start_date = db.Column(db.String(20))
    peak_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))

    # User Reported or Historical Outcome
    # OCCURRED, PARTIALLY_OCCURRED, DID_NOT_OCCUR, TOO_EARLY, UNKNOWN
    status = db.Column(db.String(30), default="PENDING")
    actual_event_date = db.Column(db.String(20))
    event_description = db.Column(db.Text)

    # Validation Source (V3.2)
    # USER_REPORTED, HISTORICAL_VERIFIED, SYNTHETIC_TEST
    source_type = db.Column(db.String(30), default="USER_REPORTED")
    verification_status = db.Column(db.String(30), default="UNVERIFIED")

    # Timing Match Categorization (Calculated post-report)
    # PEAK_HIT, ACTIVE_WINDOW_HIT, BROAD_MATCH, NO_MATCH
    timing_quality = db.Column(db.String(30))
    timing_error_days = db.Column(db.Integer) # Actual - Peak

    user_reported_confidence = db.Column(db.Integer) # 1-5
    user_notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reported_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "domain": self.domain,
            "strength": self.prediction_strength,
            "status": self.status,
            "timing_quality": self.timing_quality,
            "versions": {
                "calc": self.calculation_version,
                "dasha": self.dasha_version
            }
        }

class RemedyTask(db.Model):
    __tablename__ = 'remedy_tasks'
    id = db.Column(db.Integer, primary_key=True)
    chart_id = db.Column(db.String(36), db.ForeignKey('charts.id'), nullable=False)
    planet = db.Column(db.String(20))
    action = db.Column(db.String(200), nullable=False)
    approach = db.Column(db.String(50))
    remedy_version = db.Column(db.String(50))

    is_active = db.Column(db.Boolean, default=True)
    completion_count = db.Column(db.Integer, default=0)
    last_completed_at = db.Column(db.DateTime)
    user_outcome_notes = db.Column(db.Text)
