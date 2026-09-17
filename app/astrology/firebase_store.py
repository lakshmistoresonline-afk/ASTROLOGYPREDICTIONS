import os
from datetime import datetime
from google.cloud import firestore

def _get_db():
    return firestore.Client()

def save_chart(owner_uid: str, chart: dict) -> str:
    if not owner_uid:
        raise ValueError("AUTHENTICATION_REQUIRED: owner_uid is mandatory.")
    db = _get_db()
    doc_ref = db.collection("users").document(owner_uid).collection("charts").document()
    cid = doc_ref.id

    payload = {
        "id": cid,
        "owner_uid": owner_uid,
        "saved_at": datetime.utcnow().isoformat(),
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

def list_charts(owner_uid: str) -> list:
    if not owner_uid:
        return []
    try:
        db = _get_db()
        docs = db.collection("users").document(owner_uid).collection("charts").order_by(
            "saved_at", direction=firestore.Query.DESCENDING
        ).stream()

        results = []
        for doc in docs:
            d = doc.to_dict()
            if d:
                d["birth_datetime"] = d.get("birth_datetime", "")
                results.append(d)
        return results
    except Exception:
        return []

def get_chart(owner_uid: str, cid: str) -> dict | None:
    if not owner_uid or not cid:
        return None
    db = _get_db()
    doc = db.collection("users").document(owner_uid).collection("charts").document(cid).get()
    if doc.exists:
        return doc.to_dict()
    return None

def delete_chart(owner_uid: str, cid: str) -> bool:
    if not owner_uid or not cid:
        return False
    try:
        db = _get_db()
        db.collection("users").document(owner_uid).collection("charts").document(cid).delete()
        return True
    except Exception:
        return False
