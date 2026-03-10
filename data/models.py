"""
models.py – SQLAlchemy database models for a movie-user relationship system.

This module defines the database schema for a Flask application that manages
users, movies, and their relationships using SQLAlchemy ORM. It implements a
many-to-many relationship between users and movies through an association table.

Key Features:
-------------
- **User Management**: Stores user information with unique identifiers.
- **Movie Catalog**: Maintains a collection of movies with metadata.
- **User-Movie Relationships**: Tracks which users have which movies
- **Cascading Deletes**: Automatically handles cleanup of orphaned relationship records.
- **String Representations**: Provides both developer-friendly (`__repr__`) and
    user-friendly (`__str__`) output.

Database Schema:
----------------
    UserMovies (Association Table):
        - user_id (FK): References the User table.
        - movie_id (FK): References the Movie table.
        - added_at: When the film was added
        - Composite primary key (user_id, movie_id).

    User:
        - id: Auto-incrementing primary key.
        - name: User's display name (max 100 chars, required).
        - user_movies_link: One-to-many relationship to UserMovies.

    Movie:
        - id: Auto-incrementing primary key.
        - title: Movie title (max 200 chars, required).
        - director: Director's name (max 100 chars, required).
        - year: Release year (required).
        - poster_url: Optional URL to movie poster image.
        - movie_users_link: One-to-many relationship to UserMovies.

Relationships:
--------------
- Many-to-Many: Users ↔ Movies (via UserMovies association table).
- Bidirectional: Both User and Movie classes have back-references to the association table.
"""
from typing import List, Optional
from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy's declarative mapping.

    Serves as the root for all database models, providing the registry
    that tracks and manages the database schema and table metadata.
    """


db = SQLAlchemy(model_class=Base)


class UserMovies(db.Model):
    """
    Association model representing the relationship between a User and a Movie.
    Named 'UserMovies' to clearly indicate the link between the two entities.

    Attributes:
        user_id (int): Foreign key referencing the user. Part of the composite primary key.
        movie_id (int): Foreign key referencing the movie. Part of the composite primary key.
        user (User): Relationship back to the User instance.
        movie (Movie): Relationship back to the Movie instance.
    """
    __tablename__ = "user_movies"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    added_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    # Relationships to the parent models
    user: Mapped["User"] = relationship(back_populates="user_movies_link")
    movie: Mapped["Movie"] = relationship(back_populates="movie_users_link")

    def __repr__(self):
        """
        Return a developer-friendly string representation of the UserMovies link.

        Useful for debugging in the console or logs to quickly identify
        which user is linked to which movie.
        """
        return f"<UserMovies(user_id={self.user_id}, movie_id={self.movie_id})>"

    def __str__(self):
        """
        Return a human-readable string describing the relationship.

        This provides a simple textual summary of the connection
        between a user and their liked movie.
        """
        return f"User {self.user_id} likes Movie {self.movie_id}"


class User(db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (int): Unique identifier and primary key for the user.
        name (str): The display name or username, limited to 100 characters.
        user_movies_link (List[UserMovies]): A list of association objects
            linking this user to their favorite movies.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    user_movies_link: Mapped[List["UserMovies"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    @property
    def favorite_movies(self) -> List["Movie"]:
        """
        Convenience property to access movies directly.
        Usage: user.favorite_movies
        """
        return [link.movie for link in self.user_movies_link]

    def __repr__(self):
        """
        Return a developer-friendly representation of the User instance.

        Includes the unique ID and the name to make it easy to distinguish
        between user objects during debugging or in logs.
        """
        return f"<User(id={self.id}, name='{self.name}')>"

    def __str__(self):
        """
        Return the human-readable representation of the user.

        This is used for simple display purposes, such as in templates
        or when the user object is printed directly.
        """
        return self.name


class Movie(db.Model):
    """
    Represents a movie record in the database.

    Attributes:
        id (int): Unique identifier and primary key for the movie.
        title (str): The official title of the movie (max 200 chars).
        director (str): The director of the movie (max 100 chars).
        year (int): The release year.
        poster_url (Optional[str]): A link to the movie poster image.
        movie_users_link (List[UserMovies]): A list of association objects
            tracking which users have added this movie to their favorites.
    """
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    director: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    poster_url: Mapped[Optional[str]] = mapped_column(String(500))

    movie_users_link: Mapped[List["UserMovies"]] = relationship(
        back_populates="movie", cascade="all, delete-orphan"
    )

    def __repr__(self):
        """
        Return a developer-friendly representation of the Movie instance.

        Includes the unique ID, title, and release year to help identify
        specific movie records during debugging.
        """
        return f"<Movie(id={self.id}, title='{self.title}', year={self.year})>"

    def __str__(self):
        """
        Return a human-readable representation of the movie.

        This is used for display purposes, such as in UI dropdowns or
        lists, showing the title followed by the release year.
        """
        return f"{self.title} ({self.year})"
