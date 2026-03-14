"""
app.py – Main application module for the Movie Collection Manager.

This Flask-based web application allows users to manage their personal movie collections,
search for movies using the OMDb API, and customize movie titles in their collections.
It provides a complete CRUD interface for users and their movie relationships,
with proper error handling and user feedback.

Key Features:
-------------
- **User Management**: Create and view user accounts.
- **Movie Collection**: Add, view, update, and remove movies from user collections.
- **OMDb Integration**: Search for movies using the OMDb API and add them to collections.
- **Title Customization**: Allow users to override movie titles in their personal collections.
- **Error Handling**: Comprehensive error handling with user-friendly flash messages.
- **Database Initialization**: Automatic database table creation on first run.

Routes:
-------
    / (GET):
        Displays all registered users.

    /users (POST):
        Creates a new user.

    /users/<user_id>/movies (GET/POST):
        Views a user's movie collection or adds new movies via IMDb ID.

    /users/<user_id>/omdb_result (POST):
        Searches for movies via OMDb API and displays results.

    /users/<user_id>/movies/<movie_id>/update (GET/POST):
        Updates the custom title for a movie in a user's collection.

    /users/<user_id>/movies/<movie_id>/delete (POST):
        Removes a movie from a user's collection.

Error Handlers:
--------------
    404 Not Found:
        Renders a custom 404 error page.

    500 Internal Server Error:
        Logs the error and renders a custom 500 error page.

Database:
---------
- Uses SQLAlchemy ORM with the following models:
  - User: Represents application users.
  - Movie: Stores movie metadata.
  - UserMovies: Association table for the many-to-many relationship between users and movies.

Initialization:
---------------
- Automatically creates database tables if they don't exist (via `init_db()`).
- Configures the Flask application using settings from `config.AppSettings`.
- Initializes the DataManager for database operations and OMDb API access.
"""
from flask import Flask, flash, render_template, request, redirect, url_for
from sqlalchemy import inspect

from data.data_manager import DataManager
from data.models import db, Movie
from config import AppSettings


app = Flask(__name__)
app.config.from_object(AppSettings)
data_manager = DataManager()
data_manager.init_app(app)
db.init_app(app)



@app.route('/')
def home():
    """
    Renders the home page, displaying all registered users.

    Fetches the user list from the DataManager. If the database retrieval fails,
    an error message is flashed and an empty list is passed to the template
    to prevent rendering errors.

    Returns:
        str: The rendered 'home.html' template with the users' data.
    """
    success, result = data_manager.get_all_users()

    if not success:
        flash(result, 'error')
        return render_template('home.html', users=[])

    return render_template('home.html', users=result)


@app.route('/users', methods=['POST'])
def add_user():
    """
    Handles the creation of a new user via form submission.

    Extracts the 'name' from the POST request. If a name is provided,
    it attempts to persist the new user via the DataManager.
    A feedback message is flashed to the user before redirecting
    to the home page.

    Returns:
        Response: A redirect to the 'home' endpoint.
    """
    user_name = request.form.get('name')

    if user_name:
        success, message = data_manager.add_user(user_name)
        flash(message, 'success' if success else 'error')

    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def users_movies(user_id):
    """
    Handles viewing the user's collection and adding new movies.

    Args:
        user_id (int): The unique identifier of the user.

    Behavior:
        - GET: Retrieves the movie list. If the collection is empty or an error
               occurs, it silently renders the page with an empty list.
        - POST: Processes an IMDb ID to add a movie. Validates the input and
                provides feedback via flash messages.

    Returns:
        Union[str, Response]: The 'movies.html' template or a redirect.
    """
    if request.method == 'GET':
        success, result = data_manager.get_all_movies(user_id)
        if not success:
            return render_template('movies.html', movies=[], user_id=user_id)
        return render_template('movies.html', movies=result, user_id=user_id)

    if request.method == 'POST':
        imdb_id = request.form.get('imdb_id')
        if not imdb_id:
            flash("Missing parameter imdb_id.", "error")
            return redirect(url_for('users_movies', user_id=user_id))

        success, message = data_manager.add_movie_by_id(user_id, imdb_id)
        flash(message, 'success' if success else 'error')
        return redirect(url_for('users_movies', user_id=user_id))


@app.route('/users/<int:user_id>/omdb_result', methods=['POST'])
def choose_movie_to_add(user_id):
    """
    Searches for movies via the OMDb API and displays potential matches.

    Args:
        user_id (int): The unique identifier of the user performing the search.

    Behavior:
        - Extracts the 'movie_title' from the form.
        - Queries the OMDb API for a list of matches.
        - If the API request fails (e.g., network error), it redirects back
          to the collection with an error message.
        - If the API succeeds but finds no movies, it flashes an info message
          and renders the results page with an empty state.

    Returns:
        Union[str, Response]: The 'omdb_result.html' template with found movies
        or a redirect on API failure.
    """
    movie_title = request.form.get('movie_title')
    success, result = data_manager.search_movie_at_omdb(movie_title)
    if not success:
        flash(f"API Error: {result}", "error")
        return redirect(url_for('users_movies', user_id=user_id))

    found_movies = result.get('Search', [])
    if not found_movies:
        flash(f"No movies found for '{movie_title}'.", "info")

    return render_template(
        'omdb_result.html',
        movies=found_movies,
        user_id=user_id
    )




@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['GET', 'POST'])
def update_user_movie(user_id, movie_id):
    """
    Manages the local title override for a movie in a user's collection.

    Args:
        user_id (int): The unique identifier of the user.
        movie_id (int): The unique identifier of the movie.

    Behavior:
        - GET: Renders the update form for the specific movie entry.
        - POST: Validates the 'new_title' and updates the association in the
                database. Ensures titles are not blank.

    Returns:
        Union[str, Response]: The 'update_title.html' template or a redirect
        to the user's movie list.
    """
    success, result = data_manager.get_movie(user_id, movie_id)
    if not success:
        flash(result, "error")
        return redirect(url_for('users_movies', user_id=user_id))

    if request.method == 'GET':
        return render_template('update_title.html', movie=result, user_id=user_id)

    if request.method == 'POST':
        new_title = request.form.get('new_title')
        if not new_title:
            flash("The title cannot be blank!", "error")
            return redirect(url_for('update_user_movie', user_id=user_id, movie_id=movie_id))

        success, result = data_manager.user_movie_title_override(user_id, result, new_title)
        if not success:
            flash(result, "error")
            return redirect(url_for('users_movies', user_id=user_id))

        flash(result, "success")
        return redirect(url_for('users_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_user_movie(user_id, movie_id):
    """
    Removes a specific movie from a user's collection.

    The route first verifies that the movie exists in the user's collection
    via the data manager, then proceeds to delete the association.

    Args:
        user_id (int): The unique identifier of the user.
        movie_id (int): The unique identifier of the movie to be removed.

    Returns:
        Response: Redirects to the user's movie list with a success or
                  error message flashed to the user.
    """
    success, result = data_manager.get_movie(user_id, movie_id)
    if not success:
        flash(result, "error")
        return redirect(url_for('users_movies', user_id=user_id))

    success, message = data_manager.delete_movie(user_id, result)
    flash(message, "success" if success else "error")
    return redirect(url_for('users_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(error):
    """
    Handles 404 Not Found errors by rendering a custom error page.

    Args:
        error: The exception instance raised.

    Returns:
        tuple: A tuple containing the rendered 404.html template
               and the 404 status code.
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    """
    Handles 500 Internal Server Error by logging the exception
    and rendering a custom error page.

    Args:
        error: The exception instance raised by the server.

    Returns:
        tuple: A tuple containing the rendered 500.html template
               and the 500 status code.
    """
    app.logger.error(f"Server Error: {error}")
    return render_template('500.html'), 500


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

        if not inspector.has_table("user_movies"):
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
