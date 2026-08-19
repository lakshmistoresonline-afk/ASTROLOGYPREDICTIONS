"""
Firebase Firestore persistence for Kundli charts.
Used when deployed to Cloud Run/Firebase.
"""
import os
from datetime import datetime
from google.cloud import firestore

# Initialize Firestore
# It will use Application Default Credentials (ADC) in Cloud Run
def _get_db():
    return firestore.Client()

CHARTS_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "charts")

def save_chart(chart: dict) -> str:
    """Persist a chart dict to Firestore and return its unique ID."""
    db = _get_db()
    cid = chart.get("id") or firestore.INCREMENT  # Firestore will generate ID if not provided
    doc_ref = db.collection(CHARTS_COLLECTION).document()
    cid = doc_ref.id
    # ...

    payload = {
        "id": cid,
        "saved_at": datetime.now().isoformat(),
        "name": chart.get("name", "Unknown"),
        "place": chart.get("place", ""),
        "birth_datetime": chart.get("birth_datetime", ""),
        "timezone": chart.get("timezone", ""),
        "latitude": chart.get("latitude", 0),
        "longitude_coord": chart.get("longitude_coord", 0),
        "lagna": chart.get("lagna", {}),
        "planets": chart.get("planets", {}),
        "houses": chart.get("houses", []),
        "house_occupants": chart.get("house_occupants", {}),
        "navamsa": chart.get("navamsa", {}),
        "ayanamsa": chart.get("ayanamsa", 0),
    }

    doc_ref.set(payload)
    return cid

def list_charts() -> list:
    """Return all saved charts from Firestore sorted by saved_at."""
    db = _get_db()
    docs = db.collection(CHARTS_COLLECTION).order_by(
        "saved_at", direction=firestore.Query.DESCENDING
    ).stream()

    return [doc.to_dict() for doc in docs]

def get_chart(cid: str) -> dict | None:
    db = _get_db()
    doc = db.collection(CHARTS_COLLECTION).document(cid).get()
    if doc.exists:
        return doc.to_dict()
    return None

def delete_chart(cid: str) -> bool:
    try:
        db = _get_db()
        db.collection(CHARTS_COLLECTION).document(cid).delete()
        return True
    except Exception:
        return False
