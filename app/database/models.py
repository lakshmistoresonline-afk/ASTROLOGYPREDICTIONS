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
    dob = db.Column(db.String(20)) # YYYY-MM-DD
    tob = db.Column(db.String(10)) # HH:MM
    place = db.Column(db.String(200))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    tz = db.Column(db.String(50))

    # Store raw calculation data as JSON
    raw_data = db.Column(db.Text)

    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_data(self, data: dict):
        self.raw_data = json.dumps(data, default=str)

    def get_data(self) -> dict:
        if self.raw_data:
            return json.loads(self.raw_data)
        return {}
