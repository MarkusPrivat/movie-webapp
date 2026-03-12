from sqlalchemy import select

from data.models import db, User, Movie, UserMovies
from messages import UserMessages


class DataManager():
    #TODO: Define Crud operations as methods
    def __init__(self):
        pass

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


    def get_movies(self, user_id):
        #TODO: Gibt eine Liste aller Filme eines bestimmten Nutzers zurück.
        stmt = (
            select(Movie)
            .join(UserMovies)
            .where(UserMovies.user_id == user_id)
        )
        movies = db.session.execute(stmt).scalars().all()
        return movies

    def add_movie(self, movie):
        #TODO: Fügt einen neuen Film zu den Favoriten eines Nutzers hinzu. Der Vorgang ist ähnlich wie beim Hinzufügen eines neuen Nutzers.
        already_added = any(link.movie_id == movie.id for link in self.user_movies_link)

        if not already_added:
            new_link = UserMovies(user=self, movie=movie)
            self.user_movies_link.append(new_link)

    def update_movie(self, movie_id, new_title):
        #TODO: Aktualisiere die Details eines bestimmten Films in der Datenbank.
        pass

    def update_details(self, new_title: str = None, new_director: str = None, new_year: int = None):
        if new_title:
            self.title = new_title
        if new_director:
            self.director = new_director
        if new_year:
            self.year = new_year

    def delete_movie(self, movie_id):
        #TODO: Entferne den Film aus der Favoritenliste des Nutzers.
        self.user_movies_link = [
            link for link in self.user_movies_link
            if link.movie_id != movie_id
        ]
