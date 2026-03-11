from sqlalchemy import select

from models import db, User, Movie

class DataManager():
    #TODO: Define Crud operations as methods
    def __init__(self):
        pass

    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        #TODO: Gibt eine Liste aller Nutzer in deiner Datenbank zurück
        users = db.session.execute(select(User.name).order_by(User.id)).scalars().all()
        return users

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
