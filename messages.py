from dataclasses import dataclass

@dataclass(frozen=True)
class UserMessages:
    CREATE_SUCCESS = "User successfully created."
    CREATE_ERROR = "Error adding user:"
    GET_ALL_USER_ERROR = "Error fetching users:"


@dataclass(frozen=True)
class MovieMessages:
    GET_ALL_MOVIES_ERROR = "Error fetching movies:"
    GET_MOVIE_ERROR = "Error fetching movie:"
    ALREADY_IN_COLLECTION = "This movie is already in your collection."
    NOT_IN_COLLECTION = "Movie not in your collection."
    NO_MOVIE_IN_COLLECTION = "You have no movies in your collection"
    ADD_SUCCESS = "Successfully added to your collection."
    ADD_ERROR = "Error saving movie:"
    TITLE_UPDATE = "Title updated for your collection."