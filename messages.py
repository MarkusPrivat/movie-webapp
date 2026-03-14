"""
messages.py – Centralized message constants for consistent user feedback.

This module defines immutable dataclasses containing standardized message strings
for all user-facing notifications in the application. By centralizing these messages,
it ensures consistent terminology and phrasing across the entire application,
simplifying maintenance and internationalization efforts.

Key Features:
-------------
- **Immutable Message Constants**: Uses frozen dataclasses to prevent accidental modification.
- **Categorized Messages**: Organizes messages by domain (users vs. movies).
- **Consistent UI Feedback**: Guarantees uniform error/success messages throughout the application.
- **Easy Maintenance**: All user-facing text is defined in one location.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class UserMessages:
    """
    Centralized store for user-related feedback messages.

    This class provides standardized strings for operations involving
    user management, ensuring consistent UI feedback across the application.
    """
    CREATE_SUCCESS = "User successfully created."
    CREATE_ERROR = "Error adding user:"
    GET_ALL_USER_ERROR = "Error fetching users:"


@dataclass(frozen=True)
class MovieMessages:
    """
    Centralized store for movie-related feedback and error messages.

    Contains pre-defined messages for collection management, API results,
    and database operations. Using these constants ensures that
    success and error notifications remain consistent.
    """
    GET_ALL_MOVIES_ERROR = "Error fetching movies:"
    GET_MOVIE_ERROR = "Error fetching movie:"
    ALREADY_IN_COLLECTION = "This movie is already in your collection."
    NOT_IN_COLLECTION = "Movie not found in your collection."
    NO_MOVIE_IN_COLLECTION = "You have no movies in your collection"
    ADD_SUCCESS = "Successfully added to your collection."
    ADD_ERROR = "Error saving movie:"
    TITLE_UPDATE = "Title updated for your collection."
    REMOVE_SUCCESS = "Movie removed successfully."
    REMOVE_ERROR = "Error deleting movie:"
