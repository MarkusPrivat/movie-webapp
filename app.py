from flask import Flask, flash, render_template, request, redirect, url_for
from sqlalchemy import inspect

from data.data_manager import DataManager
from data.models import db, Movie
from config import AppSettings


app = Flask(__name__)
app.config.from_object(AppSettings)

db.init_app(app)
data_manager = DataManager()


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


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def users_movies():
    # TODO: Wenn du auf einen Nutzernamen klickst, ruft die App die Liste der
    #       Lieblingsfilme dieses Nutzers ab und zeigt sie an.
    pass


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_users_movie():
    # TODO: Fügt einen neuen Film zur Favoritenliste eines Nutzers hinzu.
    pass


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
