import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


class AppSettings:
    """Base app configuration."""
    PROJECT_ROOT = Path(__file__).resolve().parent
    DATABASE_PATH = PROJECT_ROOT / "data" / "data.sqlite"

    # Flask & SQLAlchemy
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH.as_posix()}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OMDb API
    OMDB_API_KEY = os.getenv('OMDB_API_KEY')
    OMDB_API_BASE_URL = "https://www.omdbapi.com/?"

    if not SECRET_KEY:
        raise ValueError("FLASK_SECRET_KEY nicht in der .env gefunden!")
    if not OMDB_API_KEY:
        raise ValueError("OMDB_API_KEY nicht in der .env gefunden!")
