import os
from functools import wraps
from typing import Optional, Dict, Any
from datetime import datetime
from flask import request, jsonify, session, g, redirect, url_for
from ..database.models import db, UserAccount

def verify_firebase_id_token(id_token: str) -> Optional[Dict[str, Any]]:
    """
    Production Firebase ID token verification using firebase-admin SDK.
    In testing environment only, supports mock tokens.
    Returns decoded token dict (containing 'uid', 'email', 'email_verified', 'name') or None.
    """
    if not id_token:
        return None

    if os.getenv("FLASK_ENV") == "testing" and id_token.startswith("mock_token_"):
        mock_uid = id_token.replace("mock_token_", "")
        return {
            "uid": mock_uid,
            "email": f"{mock_uid}@astropredictions.app",
            "email_verified": True,
            "name": "Test User"
        }

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

        decoded_token = auth.verify_id_token(id_token, check_revoked=True)
        return decoded_token
    except Exception:
        return None

def get_current_authenticated_user() -> Optional[Dict[str, Any]]:
    """Resolves verified Firebase identity from session or Authorization Bearer token."""
    token = session.get("firebase_id_token")
    if token:
        claims = verify_firebase_id_token(token)
        if claims:
            return claims

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        id_token = auth_header.split(" ")[1]
        claims = verify_firebase_id_token(id_token)
        if claims:
            session["firebase_id_token"] = id_token
            session["firebase_uid"] = claims.get("uid")
            return claims
    return None

def get_current_user_uid() -> Optional[str]:
    claims = get_current_authenticated_user()
    if claims:
        return claims.get("uid")
    return session.get("firebase_uid")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        claims = get_current_authenticated_user()
        if not claims:
            if request.path.startswith("/api/"):
                return jsonify({"error": "AUTHENTICATION_REQUIRED", "message": "Valid Firebase authentication required."}), 401
            return redirect(url_for("marketing.home", next=request.path))

        uid = claims.get("uid")
        email = claims.get("email")
        email_verified = claims.get("email_verified", False)
        display_name = claims.get("name") or claims.get("display_name")

        user = UserAccount.query.filter_by(firebase_uid=uid).first()
        if not user:
            if not email:
                return jsonify({"error": "INVALID_IDENTITY", "message": "Verified email required from identity provider."}), 400
            user = UserAccount(
                firebase_uid=uid,
                email=email,
                email_verified=email_verified,
                display_name=display_name,
                status="active"
            )
            db.session.add(user)
            db.session.commit()
        else:
            user.email = email
            user.email_verified = email_verified
            if display_name:
                user.display_name = display_name
            user.last_login_at = datetime.utcnow()
            db.session.commit()

        g.current_user = user
        g.firebase_uid = uid
        return f(*args, **kwargs)
    return decorated_function
