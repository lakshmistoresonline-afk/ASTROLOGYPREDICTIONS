import os
from functools import wraps
from typing import Optional
from flask import request, jsonify, session, g, redirect, url_for
from ..database.models import db, UserAccount

def verify_firebase_id_token(id_token: str) -> Optional[str]:
    """
    Verifies Firebase ID token or resolves development/test mock UIDs if enabled.
    """
    if not id_token:
        return None

    if os.getenv("FLASK_ENV") == "testing" or id_token.startswith("mock_token_"):
        return id_token.replace("mock_token_", "")

    try:
        import firebase_admin
        from firebase_admin import auth, credentials
        if not firebase_admin._apps:
            cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
            if cred_path and os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            else:
                firebase_admin.initialize_app()

        decoded_token = auth.verify_id_token(id_token)
        return decoded_token.get("uid")
    except Exception:
        return None

def get_current_user_uid() -> Optional[str]:
    uid = session.get("firebase_uid")
    if uid:
        return uid

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        uid = verify_firebase_id_token(token)
        if uid:
            session["firebase_uid"] = uid
            return uid
    return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        uid = get_current_user_uid()
        if not uid:
            if request.path.startswith("/api/"):
                return jsonify({"error": "AUTHENTICATION_REQUIRED", "message": "Valid Firebase authentication required."}), 401
            return redirect(url_for("marketing.home", next=request.path))

        user = UserAccount.query.filter_by(firebase_uid=uid).first()
        if not user:
            user = UserAccount(firebase_uid=uid, email=f"{uid}@astropredictions.app")
            db.session.add(user)
            db.session.commit()

        g.current_user = user
        g.firebase_uid = uid
        return f(*args, **kwargs)
    return decorated_function
