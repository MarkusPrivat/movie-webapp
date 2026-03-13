from sqlalchemy import select

from data.models import db, User, Movie, UserMovies
from external_apis.omdb_api import OMDbAPI
from messages import UserMessages, MovieMessages


class DataManager():
    #TODO: Define Crud operations as methods
    def __init__(self):
        """
        Initializes the DataManager instance.

        Attributes:
            omdb_api (Optional[OMDbAPI]): A reference to the OMDb API service
                used for fetching external movie data. Initially set to None
                until the service is properly initialized.
        """
        self.omdb_api = None


    def init_app(self, app):
        """
        Initializes the DataManager with configuration from the Flask app.

        Args:
            app (Flask): The Flask application instance containing the
                necessary configuration keys like 'OMDB_API_KEY' and
                'OMDB_API_BASE_URL'.

        Sets:
            self.omdb_api (OMDbAPI): An initialized instance of the OMDbAPI
                service using the provided configuration.
        """
        api_key = app.config.get('OMDB_API_KEY')
        base_url = app.config.get('OMDB_API_BASE_URL')
        self.omdb_api = OMDbAPI(api_key, base_url)


    def add_user(self, name: str) -> tuple[bool, str]:
        """
        Adds a new user to the database.

        Attempts to create a User instance and commit it to the database.
        If an error occurs during the process, the transaction is rolled back.

        Args:
            name (str): The name of the user to be created.

        Returns:
            tuple[bool, str]:
                - (True, UserMessages.CREATE_SUCCESS) on successful creation.
                - (False, error_message) if an exception occurs during the database operation.
        """
        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
            return True, UserMessages.CREATE_SUCCESS
        except Exception as error:
            db.session.rollback()
            return False, f"{UserMessages.CREATE_ERROR} '{error}'"


    def get_all_users(self) -> tuple[bool, list[User] | str]:
        """
        Retrieves a list of all users from the database.

        Returns:
            tuple[bool, list[User] | str]:
                - (True, list_of_users) on success.
                - (False, error_message) if an exception occurs during the database query.
        """
        try:
            stmt = (
                select(User)
                .order_by(User.id)
            )
            users = db.session.execute(stmt).scalars().all()
            return True, users
        except Exception as error:
            return False, f"{UserMessages.GET_ALL_USER_ERROR} '{error}'"


    def get_all_movies(self, user_id: int) -> tuple[bool, list[Movie] | str]:
        """
        Retrieves a list of all movies associated with a specific user,
        ordered alphabetically by title.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            tuple[bool, list[Movie] | str]:
                - A tuple where the first element indicates success (True/False).
                - The second element is a list of Movie objects if successful,
                  or an error message string if no movies are found or an
                  exception occurs.
        """
        try:
            stmt = (
                select(UserMovies, Movie)
                .join(Movie)
                .where(UserMovies.user_id == user_id)
                .order_by(Movie.title)
            )
            movies = db.session.execute(stmt).all()

            if not movies:
                return False, MovieMessages.NOT_IN_COLLECTION

            return True, movies
        except Exception as error:
            return False, f"{MovieMessages.GET_ALL_MOVIES_ERROR} '{error}'"


    def get_movie(self, user_id: int, movie_id: int) -> tuple[bool, Movie | str]:
        """
        Retrieves a specific movie associated with a specific user.

        Args:
            user_id (int): The unique identifier of the user.
            movie_id (int): The unique identifier of the movie.

        Returns:
            tuple[bool, Movie | str]:
                - A tuple where the first element indicates success (True/False).
                - The second element is a Movie object if successful,
                  or an error message string if the request fails or an exception occurs.
        """
        try:
            stmt = (
                select(Movie)
                .join(UserMovies)
                .where(UserMovies.user_id == user_id)
                .where(UserMovies.movie_id == movie_id)
            )
            movie = db.session.execute(stmt).scalars().first()

            if not movie:
                return False, MovieMessages.NOT_IN_COLLECTION

            return True, movie
        except Exception as error:
            return False, f"{MovieMessages.GET_MOVIE_ERROR} '{error}'"


    def search_movie_at_omdb(self, movie_title: str) -> tuple[bool, dict | str]:
        """
        Queries the OMDb API for movies matching a given title.

        Args:
            movie_title (str): The search query string for the movie title.

        Returns:
            tuple[bool, dict | str]:
                - A tuple where the first element indicates success (True/False).
                - The second element is a dictionary containing the search results
                  if successful, or an error message string if the API call failed.
        """
        success, result = self.omdb_api.search_movie_title(movie_title)
        if not success:
            return False, result
        return True, result


    def add_movie_by_id(self, user_id: int, imdb_id: str) -> tuple[bool, str]:
        """
        Adds a movie to a user's collection by fetching details from OMDb.

        Args:
            user_id (int): The unique identifier of the user.
            imdb_id (str): The unique IMDb identifier for the movie.

        Behavior:
            1. Fetches movie details from the OMDb API via 'omdb_api'.
            2. Ensures the movie exists in the database using '_get_or_create_movie'.
            3. Links the movie to the user using '_link_movie_to_user'.
            4. Performs a database rollback in case of any exceptions to
               ensure data integrity.

        Returns:
            tuple[bool, str]:
                - A tuple where the first element indicates success (True/False).
                - A message string describing the result or any error occurred.
        """
        try:
            success, result = self.omdb_api.get_movie_by_id(imdb_id)
            if not success:
                return False, f"API Error: {result}"

            movie = self._get_or_create_movie(imdb_id, result)
            return self._link_movie_to_user(movie, user_id)

        except Exception as error:
            db.session.rollback()
            return False, f"{MovieMessages.ADD_ERROR} {str(error)}"


    def _get_or_create_movie(self, imdb_id: str, movie_data) -> Movie:
        """
        Retrieves a movie from the database or creates it if it doesn't exist.

        Args:
            imdb_id (str): The unique IMDb identifier used to search the database.
            movie_data (dict): A dictionary containing movie details (Title,
                Year, Director, Poster) returned from the OMDb API.

        Returns:
            Movie: The 'Movie' database object, either fetched or newly created.
        """
        movie = db.session.query(Movie).filter_by(imdb_id=imdb_id).first()
        if not movie:
            movie = Movie(
                title=movie_data.get('Title'),
                year=int(movie_data.get('Year', 0)),
                director=movie_data.get('Director'),
                poster_url=movie_data.get('Poster'),
                imdb_id=imdb_id
            )
            db.session.add(movie)
            db.session.commit()
        return movie


    def _link_movie_to_user(self, movie: Movie, user_id: int) -> tuple[bool, str]:
        """
        Creates an association between a user and a movie if it doesn't already exist.

        Args:
            movie (Movie): The movie instance to be linked.
            user_id (int): The unique identifier of the user.

        Returns:
            tuple[bool, str]:
                - A tuple indicating success (True/False).
                - A message string (MovieMessages.ADD_SUCCESS or
                  MovieMessages.ALREADY_IN_COLLECTION).
        """
        if self._get_user_movie_link(movie, user_id):
            return False, MovieMessages.ALREADY_IN_COLLECTION

        new_link = UserMovies(user_id=user_id, movie_id=movie.id)
        db.session.add(new_link)
        db.session.commit()
        return True, MovieMessages.ADD_SUCCESS

    def _get_user_movie_link(self, movie: Movie, user_id: int) -> UserMovies | None:
        """
        Retrieves the association link between a user and a movie.

        Args:
            movie (Movie): The movie instance to check.
            user_id (int): The unique identifier of the user.

        Returns:
            UserMovies | None: The association object if it exists, otherwise None.
        """
        return db.session.query(UserMovies).filter_by(
            user_id=user_id,
            movie_id=movie.id
        ).first()

    def user_movie_title_override(
            self,
            user_id: int,
            movie: Movie,
            new_title: str) -> tuple[bool, str]:
        """
        Updates the local title override for a specific movie in a user's collection.

        Args:
            user_id (int): The unique identifier of the user.
            movie (Movie): The movie instance to be updated.
            new_title (str): The new title to be set for this specific user.

        Returns:
            tuple[bool, str]:
                - A tuple indicating success (True/False).
                - A message string describing the outcome of the update operation.
        """
        user_movie_link = self._get_user_movie_link(movie, user_id)
        if not user_movie_link:
            return False, MovieMessages.NOT_IN_COLLECTION

        user_movie_link.user_title_override = new_title
        db.session.commit()
        return True, MovieMessages.TITLE_UPDATE

    def delete_movie(self, user_id: int, movie: Movie) -> tuple[bool, str]:
        """
        Removes a movie from a user's collection by deleting the association link.

        Args:
            movie (Movie): The movie object to be removed.
            user_id (int): The unique identifier of the user.

        Returns:
            tuple[bool, str]:
                - A tuple where the first element indicates success (True/False).
                - The second element is a success or error message string.
        """
        try:
            user_movie_link = self._get_user_movie_link(movie, user_id)
            if not user_movie_link:
                return False, MovieMessages.NOT_IN_COLLECTION

            db.session.delete(user_movie_link)
            db.session.commit()
            return True, MovieMessages.REMOVE_SUCCESS
        except Exception as error:
            db.session.rollback()
            return False, f"{MovieMessages.REMOVE_ERROR} {error}"
