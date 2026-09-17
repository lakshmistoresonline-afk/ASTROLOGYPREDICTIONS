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
    owner_uid = db.Column(db.String(128), index=True, nullable=True) # Firebase UID ownership bridge
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

    group_id = db.Column(db.String(20), default="BETA_GROUP_1")
    participant_id = db.Column(db.String(50))
    session_id = db.Column(db.String(50))

    engine_version = db.Column(db.String(20), default="V3.15")
    calculation_version = db.Column(db.String(50))
    dasha_version = db.Column(db.String(50))
    transit_version = db.Column(db.String(50))
    evidence_version = db.Column(db.String(50))
    remedy_version = db.Column(db.String(50))
    timing_calibration_version = db.Column(db.String(50), default="V3.15")

    domain = db.Column(db.String(50), nullable=False)
    event_type = db.Column(db.String(50))
    event_magnitude = db.Column(db.String(20))
    what_may_develop = db.Column(db.Text)

    prediction_strength = db.Column(db.String(20))
    engine_confidence = db.Column(db.String(20))

    signal_score = db.Column(db.Float)
    quality_score = db.Column(db.Float)
    calibrated_probability = db.Column(db.Float)

    prediction_text = db.Column(db.Text, nullable=False)
    possible_manifestations = db.Column(db.Text)
    confirmation_criteria = db.Column(db.Text)
    what_to_do = db.Column(db.Text)
    remedy_text = db.Column(db.Text)
    evidence_snapshot = db.Column(db.Text)

    start_date = db.Column(db.String(20))
    peak_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    timing_phase = db.Column(db.String(30))
    proximity_weight = db.Column(db.Float)

    status = db.Column(db.String(30), default="PENDING")
    actual_event_date = db.Column(db.String(20))
    actual_event_end_date = db.Column(db.String(20))
    event_description = db.Column(db.Text)

    verification_level = db.Column(db.String(30), default="SELF_REPORTED")

    timing_quality = db.Column(db.String(30))
    timing_error_days = db.Column(db.Integer)
    lead_time_days = db.Column(db.Integer)

    user_reported_confidence = db.Column(db.Integer)
    user_notes = db.Column(db.Text)
    practitioner_feedback = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reported_at = db.Column(db.DateTime)

    source_type = db.Column(db.String(30), default="BETA_SESSION")
    cohort = db.Column(db.String(30))
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
    id = db.Column(db.String(36), primary_key=True)
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

    status = db.Column(db.String(30))
    engine_version = db.Column(db.String(20), default="V3.17")

    actual_event_date = db.Column(db.String(20))
    matching_status = db.Column(db.String(30), default="UNKNOWN")
    timing_error_days = db.Column(db.Integer)
    matching_version = db.Column(db.String(30))
    integrity_reason = db.Column(db.String(100))

    cohort = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Durable Immutable Report Persistence (P0.4)
class ReportRecord(db.Model):
    __tablename__ = 'report_records'
    report_id = db.Column(db.String(36), primary_key=True)
    owner_uid = db.Column(db.String(128), index=True, nullable=False)
    chart_id = db.Column(db.String(36), nullable=False)
    report_type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200))
    content_json = db.Column(db.Text, nullable=False)
    evidence_snapshot_json = db.Column(db.Text)
    engine_version = db.Column(db.String(20), default="P0.3-R42")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Monetization & Commercial Models
class UserAccount(db.Model):
    __tablename__ = 'user_accounts'
    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(128), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120))
    email_verified = db.Column(db.Boolean, default=False)
    display_name = db.Column(db.String(100))
    status = db.Column(db.String(30), default="active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    subscriptions = db.relationship('SubscriptionRecord', backref='user', lazy=True)
    orders = db.relationship('OrderRecord', backref='user', lazy=True)
    entitlements = db.relationship('EntitlementRecord', backref='user', lazy=True)

class SubscriptionRecord(db.Model):
    __tablename__ = 'subscription_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_accounts.id'), nullable=False)
    provider = db.Column(db.String(30), default="razorpay")
    provider_subscription_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(30), default="active")
    plan_type = db.Column(db.String(30), default="plus_monthly")
    renews_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class OrderRecord(db.Model):
    __tablename__ = 'order_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_accounts.id'), nullable=True)
    product_id = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default="INR")
    status = db.Column(db.String(30), default="pending")
    provider_order_id = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PaymentRecord(db.Model):
    __tablename__ = 'payment_records'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order_records.id'), nullable=False)
    provider_payment_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(30), default="success")
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EntitlementRecord(db.Model):
    __tablename__ = 'entitlement_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_accounts.id'), nullable=False)
    feature_name = db.Column(db.String(50), nullable=False)
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AttributionRecord(db.Model):
    __tablename__ = 'attribution_records'
    id = db.Column(db.Integer, primary_key=True)
    anonymous_id = db.Column(db.String(64), index=True)
    first_touch_source = db.Column(db.String(50), default="direct")
    first_touch_medium = db.Column(db.String(50), default="none")
    last_touch_source = db.Column(db.String(50), default="direct")
    last_touch_medium = db.Column(db.String(50), default="none")
    campaign = db.Column(db.String(100))
    referral_code = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AnalyticsEventLog(db.Model):
    __tablename__ = 'analytics_event_logs'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50), nullable=False, index=True)
    anonymous_id = db.Column(db.String(64))
    properties_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
