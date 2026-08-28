import os
from app import create_app, db

def init():
    os.environ["FLASK_SECRET_KEY"] = "init-key"
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database schema V1.0.0 initialized.")

if __name__ == "__main__":
    init()
