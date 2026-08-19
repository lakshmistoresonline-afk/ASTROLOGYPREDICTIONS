from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from .database.models import db

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "kundli-vedic-secret-2024")

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
    CORS(app)

    # Expose LLM config to templates via config.get(...)
    app.config["LLM_BASE_URL"] = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
    app.config["LLM_MODEL"]    = os.getenv("LLM_MODEL", "")  # empty = AI notes off by default

    from .routes import main
    app.register_blueprint(main)

    return app
