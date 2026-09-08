from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_holdout = db.Column(db.Boolean, default=False)
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
    Immutable Prediction Snapshot & Outcome Tracking (V3.15).
    Stores engine versions to ensure reproducibility.
    """
    __tablename__ = 'prediction_outcomes'
    id = db.Column(db.Integer, primary_key=True)
    chart_id = db.Column(db.String(36), db.ForeignKey('charts.id'), nullable=False)

    # Beta Governance (V3.15)
    group_id = db.Column(db.String(20), default="BETA_GROUP_1")
    participant_id = db.Column(db.String(50))
    session_id = db.Column(db.String(50))

    # Engine Versions
    engine_version = db.Column(db.String(20), default="V3.15")
    calculation_version = db.Column(db.String(50))
    dasha_version = db.Column(db.String(50))
    transit_version = db.Column(db.String(50))
    evidence_version = db.Column(db.String(50))
    remedy_version = db.Column(db.String(50))
    timing_calibration_version = db.Column(db.String(50), default="V3.15")

    domain = db.Column(db.String(50), nullable=False)
    event_type = db.Column(db.String(50))
    event_magnitude = db.Column(db.String(20)) # EXCEPTIONAL, MAJOR, MODERATE
    what_may_develop = db.Column(db.Text)

    prediction_strength = db.Column(db.String(20)) # WATCH, ACTIVE, PEAK
    engine_confidence = db.Column(db.String(20)) # LOW, MODERATE, HIGH, EXTREME

    signal_score = db.Column(db.Float) # V3.22: 0-1.0 signal strength
    quality_score = db.Column(db.Float)
    calibrated_probability = db.Column(db.Float)

    prediction_text = db.Column(db.Text, nullable=False)
    possible_manifestations = db.Column(db.Text) # JSON list
    confirmation_criteria = db.Column(db.Text) # JSON list
    what_to_do = db.Column(db.Text) # Actionable guidance
    remedy_text = db.Column(db.Text) # Recommended remedy
    evidence_snapshot = db.Column(db.Text) # JSON string of all evidence items

    # Timing Snapshot
    start_date = db.Column(db.String(20))
    peak_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    timing_phase = db.Column(db.String(30)) # V3.15: SCANNING, PEAK_MANIFESTATION, etc.
    proximity_weight = db.Column(db.Float) # V3.14 metric

    # Outcome Record
    # OCCURRED, PARTIALLY_OCCURRED, DID_NOT_OCCUR, UNKNOWN, PENDING
    status = db.Column(db.String(30), default="PENDING")
    actual_event_date = db.Column(db.String(20))
    actual_event_end_date = db.Column(db.String(20))
    event_description = db.Column(db.Text)

    # Verification Level (V3.15)
    # SELF_REPORTED, PRACTITIONER_VERIFIED, DOCUMENTED, INDEPENDENTLY_VERIFIED
    verification_level = db.Column(db.String(30), default="SELF_REPORTED")

    # Metrics
    timing_quality = db.Column(db.String(30)) # PEAK_HIT, ACTIVE_WINDOW_HIT, etc.
    timing_error_days = db.Column(db.Integer)
    lead_time_days = db.Column(db.Integer) # actual_event_date - created_at

    user_reported_confidence = db.Column(db.Integer) # 1-5
    user_notes = db.Column(db.Text)
    practitioner_feedback = db.Column(db.Text) # JSON string of feedback categories

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reported_at = db.Column(db.DateTime)

    source_type = db.Column(db.String(30), default="BETA_SESSION")
    cohort = db.Column(db.String(30)) # TRAINING, VALIDATION, HOLDOUT
    integrity_reason = db.Column(db.String(100))
    matching_version = db.Column(db.String(30))

    def to_dict(self):
        return {
            "id": self.id,
            "engine": self.engine_version,
            "domain": self.domain,
            "strength": self.prediction_strength,
            "status": self.status,
            "timing_quality": self.timing_quality,
            "group": self.group_id
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

class TimelineEventSnapshot(db.Model):
    __tablename__ = 'timeline_event_snapshots'
    id = db.Column(db.String(36), primary_key=True) # event_id from TimelineEvent
    chart_id = db.Column(db.String(36), db.ForeignKey('charts.id'), nullable=False)
    domain = db.Column(db.String(50), nullable=False)
    event_type = db.Column(db.String(100))
    event_magnitude = db.Column(db.String(20))

    start_date = db.Column(db.String(20))
    peak_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))

    age_at_peak = db.Column(db.Float)

    signal_strength = db.Column(db.String(20))
    confidence = db.Column(db.String(20))

    evidence_snapshot = db.Column(db.Text)
    why_now = db.Column(db.Text)

    status = db.Column(db.String(30)) # PAST_RECONSTRUCTION, etc.
    engine_version = db.Column(db.String(20), default="V3.17")

    # Outcome tracking
    actual_event_date = db.Column(db.String(20))
    matching_status = db.Column(db.String(30), default="UNKNOWN")
    timing_error_days = db.Column(db.Integer)
    matching_version = db.Column(db.String(30))
    integrity_reason = db.Column(db.String(100))

    cohort = db.Column(db.String(30)) # TRAINING, VALIDATION, HOLDOUT
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
