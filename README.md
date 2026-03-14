# MovieWeb 🎬

A modern Flask-based web application for managing personal movie collections. The app allows users to search for movies via the **OMDb API**, add them to their private collections, and manage individual title overrides.

## 🚀 Features

* **Multi-User Support**: Create and manage multiple user profiles within a single application.
* **OMDb Integration**: Real-time movie search including posters, release years, and directors.
* **Personalized Collections**: Each user maintains their own unique movie list.
* **Title Overrides**: Users can set custom titles for movies in their collection without affecting global data.
* **Robust Error Handling**: Comprehensive protection against API timeouts, network failures, and database inconsistencies.
* **Clean Architecture**: Strictly separated layers for data management, API communication, and web presentation.

## 🛠️ Technology Stack

* **Backend:** Python 3.x, Flask
* **Database:** SQLAlchemy (SQLite)
* **API:** OMDb (Open Movie Database)
* **Frontend:** Jinja2 Templates, HTML5, CSS3

## 📂 Project Structure

```text
├── app.py              # Flask application & route controllers
├── config.py           # Central configuration & path management
├── data_manager.py     # Business logic & database orchestration
├── omdb_api.py         # Service client for the OMDb API
├── messages.py         # Centralized UI feedback strings (Dataclasses)
├── models.py           # SQLAlchemy database models (User, Movie, UserMovies)
├── .env                # Environment variables (SECRET_KEY, API_KEY)
└── data/               # SQLite database storage directory
```

⚙️ Installation & Setup
1. Clone the Repository:
```bash
git clone [https://github.com/dein-username/movieweb.git](https://github.com/dein-username/movieweb.git)
cd movieweb 
```

2. Create a Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install Dependencies:
```bash
pip install -r requirements.txt
```

4. Configure Environment Variables:
Create a .env file in the root directory:
```Code-Snippet
FLASK_SECRET_KEY=your_secret_key_here
OMDB_API_KEY=your_omdb_api_key_here
```

5. Run the Application:
```bash
python app.py
```
The application will be available at http://127.0.0.1:5002.

## 📖 Documentation
This project emphasizes readability and maintainability. All core components are documented with detailed docstrings describing technical behavior and error handling.

* **OMDbAPI:** Encapsulates HTTP requests and ensures "bulletproof" JSON parsing.
* **DataManager:** Manages complex database operations and cross-entity validation.