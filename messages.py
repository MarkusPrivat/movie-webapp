from dataclasses import dataclass

@dataclass(frozen=True)
class UserMessages:
    CREATE_SUCCESS = "User successfully created."
    CREATE_ERROR = "Error adding user:"
    GET_ALL_USER_ERROR = "Error fetching users:"


@dataclass(frozen=True)
class MovieMessages:
    GET_ALL_MOVIES_ERROR = "Error fetching movies:"
    ALREADY_IN_COLLECTION = "This movie is already in your collection."
    ADD_SUCCESS = f"Successfully added to your collection!"
    ADD_ERROR = "Error saving movie:"