from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from .database.models import db

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Security: Enforce mandatory secret key
    secret_key = os.getenv("FLASK_SECRET_KEY")
    if not secret_key:
        if os.getenv("FLASK_ENV") == "production":
            raise RuntimeError("CRITICAL: FLASK_SECRET_KEY is not set in production!")
        # In dev, we still want a warning but can fallback to a known dev-key if necessary
        # However, for highest security we should ideally fail fast.
        print("WARNING: FLASK_SECRET_KEY not found in environment. Using insecure fallback.")
        secret_key = "insecure-dev-only-key-replace-immediately"
    app.secret_key = secret_key

    # SQLite Config - Only if not using Firebase
    USE_FIREBASE = os.getenv("USE_FIREBASE", "false").lower() == "true"
    if not USE_FIREBASE:
        db_path = os.path.join(app.root_path, '..', 'data', 'app.db')
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.abspath(db_path)}"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        db.init_app(app)

        with app.app_context():
            try:
                db.create_all()
            except Exception as e:
                print(f"Warning: Could not initialize SQLite: {e}")

    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # CORS Configuration - restrict in production
    if os.getenv("FLASK_ENV") == "production":
        CORS(app, resources={r"/api/*": {"origins": os.getenv("ALLOWED_ORIGINS", "*").split(",")}} )
    else:
        CORS(app)

    # Expose LLM config to templates via config.get(...)
    app.config["LLM_BASE_URL"] = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
    app.config["LLM_MODEL"]    = os.getenv("LLM_MODEL", "")  # empty = AI notes off by default

    @app.after_request
    def add_security_headers(response):
        if os.getenv("FLASK_ENV") == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    from .routes import main
    app.register_blueprint(main)

    return app
