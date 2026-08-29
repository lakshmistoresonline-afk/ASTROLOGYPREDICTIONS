from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from .database.models import db

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Security: Enforce mandatory secret key (Phase 8 Hardening)
    secret_key = os.getenv("FLASK_SECRET_KEY")
    if not secret_key:
        raise RuntimeError(
            "CRITICAL: FLASK_SECRET_KEY is not set. "
            "Please configure it in your environment or .env file to start the application."
        )
    app.secret_key = secret_key

    # SQLite Config
    db_path = os.path.join(app.root_path, '..', 'data', 'app.db')
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.abspath(db_path)}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Could not initialize SQLite: {e}")

    app.config["TEMPLATES_AUTO_RELOAD"] = True
    CORS(app)

    # Lightweight Monitoring (Part 33)
    import logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    # Use standard logging for beta
    logging.basicConfig(filename='logs/app.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s')
    app.logger.info("Jyotish OS V1.0.0 starting...")

    from .routes import main
    from .api.tracking import tracking_bp

    app.register_blueprint(main)
    app.register_blueprint(tracking_bp)

    return app
