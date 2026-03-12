from pathlib import Path

from flask import Flask
from sqlalchemy import inspect

from data.data_manager import DataManager
from data.models import db, Movie


PROJECT_ROOT = Path(__file__).parent
DATABASE_PATH = PROJECT_ROOT / "data/data.sqlite"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_PATH.as_posix()}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "Lorem-Secret!-ipsum"

db.init_app(app)
data_manager = DataManager()

@app.route('/')
def home():
    return "Welcome to MoviWeb App!"


def init_db():
    """
    Initializes the database by creating tables if they do not exist.

    Uses an SQLAlchemy inspector to verify the existence of the 'authors' table.
    If the table is missing, it triggers the creation of all defined
    database models via SQLAlchemy's create_all() method.

    Returns:
        None
    """
    with app.app_context():
        inspector = inspect(db.engine)

        if not inspector.has_table("UserMovies"):
            print("Database tables not found. Creating tables...")
            db.create_all()
            print("Tables created successfully.")


def main():
    """
    Entry point of the application.

    Triggers the database initialization process to ensure all required
    tables exist and then starts the Flask development server in debug mode.
    """
    init_db()
    app.run(host="0.0.0.0", port=5002, debug=True)


if __name__ == "__main__":
    main()
