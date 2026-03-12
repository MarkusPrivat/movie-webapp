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
    Renders the home page, displaying a list of all registered users
    and a form to add a new user.

    Fetches user data from the DataManager. If the retrieval fails,
    an error message is flashed to the user.

    Returns:
        Response: The rendered HTML page with the list of users.
    """
    success, result = data_manager.get_all_users()

    if not success:
        flash(result, 'error')
        return render_template('home.html', users=[])

    return render_template('home.html', users=result)


@app.route('/users', methods=['POST'])
def add_user():
    """
    Handles the POST request to add a new user to the system.

    Retrieves the username from the form data and uses the DataManager
    to persist it to the database. Flashes a success or error message
    based on the outcome and redirects the user back to the home page.

    Returns:
        Response: A redirect to the 'home' route.
    """
    user_name = request.form.get('name')

    if user_name:
        success, message = data_manager.add_user(user_name)
        flash(message, 'success' if success else 'error')

    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def users_movies(user_id):
    """
    Handles the viewing and adding of movies for a specific user.

    Args:
        user_id (int): The unique identifier of the user.

    Behavior:
        GET: Retrieves the user's movie list from the data manager and
             renders the 'movies.html' template.
        POST: Adds a movie to the user's collection using its IMDb ID.
              Validates the presence of 'imdb_id' and triggers a flash
              message based on the operation's success.

    Returns:
        A rendered template for GET requests, or a redirect to the user's
        movie list for POST requests.
    """
    if request.method == 'GET':
        success, result = data_manager.get_movies(user_id)
        if not success:
            flash(result, 'error')
            return render_template('movies.html', movies=[], user_id=user_id)
        return render_template('movies.html', movies=result, user_id=user_id)

    if request.method == 'POST':
        imdb_id = request.form.get('imdb_id')
        if not imdb_id:
            flash("Missing parameter imdb_id.", "error")
            return redirect(url_for('users_movies', user_id=user_id))

        success, message = data_manager.add_movie_by_id(user_id, imdb_id
        flash(message, 'success' if success else 'error')
        return redirect(url_for('users_movies', user_id=user_id))


@app.route('/users/<int:user_id>/omdb_result', methods=['POST'])
def choose_movie_to_add(user_id):
    """
    Searches for movies via the OMDb API and displays the results.

    Args:
        user_id (int): The unique identifier of the user performing the search.

    Behavior:
        Extracts the 'movie_title' from the request form, queries the OMDb API
        via the data manager, and renders the 'omdb_result.html' template
        with the list of found movies.

        If the API call fails or no movies are found, it flashes an
        appropriate message and redirects the user back to their collection.

    Returns:
        Rendered 'omdb_result.html' template if movies are found, or a
        redirect to the user's movie list.
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




@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_user_movie():
    # TODO: Den Titel eines bestimmten Films in der Liste eines Nutzers ändern,
    #       ohne sich auf OMDb für Korrekturen zu verlassen.
    pass


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_user_movie():
    # TODO: Entfernt einen bestimmten Film aus der Liste der Lieblingsfilme eines Nutzers.
    pass



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
