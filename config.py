"""
config.py – Central configuration module for the MovieWeb application.

This module provides a structured approach to managing application settings by
loading environment variables and defining default configurations. It serves as
the single source of truth for all configuration needs across the application,
including database connections, API integrations, and security settings.

Key Features:
-------------
- **Environment Management**: Loads settings from a `.env` file using `python-dotenv`.
- **Path Resolution**: Automatically resolves project paths for database and resource files.
- **Validation**: Ensures critical configuration values are present during startup.
- **Security**: Manages sensitive credentials like API keys and secret tokens.
- **Database Configuration**: Sets up SQLite connection parameters.
- **API Integration**: Configures endpoints and credentials for external services (OMDb).

Configuration Attributes:
--------------------------
    PROJECT_ROOT (Path):
        Absolute path to the project's root directory.

    DATABASE_PATH (Path):
        Absolute path to the SQLite database file (data/data.sqlite).

    SECRET_KEY (str):
        Flask's cryptographic key for session security (loaded from FLASK_SECRET_KEY).

    SQLALCHEMY_DATABASE_URI (str):
        Connection URI for SQLAlchemy (e.g., "sqlite:///data/data.sqlite").

    SQLALCHEMY_TRACK_MODIFICATIONS (bool):
        Disabled to optimize performance (set to False).

    OMDB_API_KEY (str):
        Authentication key for the OMDb API service (loaded from OMDB_API_KEY).

    OMDB_API_BASE_URL (str):
        Base URL for OMDb API requests (default: "https://www.omdbapi.com/?").

Error Handling:
---------------
The class validates the presence of critical environment variables during
initialization and raises a `ValueError` if any required configuration is missing:

- `FLASK_SECRET_KEY`: Required for Flask session security.
- `OMDB_API_KEY`: Required for accessing the OMDb API.
"""
import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


class AppSettings:
    """
    Central configuration container for the MovieWeb application.

    This class aggregates all environment-specific and static settings required
    by Flask, SQLAlchemy, and external service clients. It handles path
    resolution for the SQLite database and enforces the presence of critical
    security credentials during startup.

    Attributes:
        PROJECT_ROOT (Path): The absolute path to the project's root directory.
        DATABASE_PATH (Path): The absolute path to the SQLite database file.
        SECRET_KEY (str): Flask's cryptographic key for session signing,
            retrieved from environment variables.
        SQLALCHEMY_DATABASE_URI (str): Formatted connection string for the
            SQLAlchemy engine.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disabled to reduce memory overhead
            by not tracking object changes.
        OMDB_API_KEY (str): Authentication key for the OMDb API service.
        OMDB_API_BASE_URL (str): The primary endpoint for OMDb API requests.

    Raises:
        ValueError: If essential environment variables ('FLASK_SECRET_KEY' or
            'OMDB_API_KEY') are missing.
    """
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
