from dataclasses import dataclass

@dataclass(frozen=True)
class UserMessages:
    CREATE_SUCCESS = "User successfully created."
    CREATE_ERROR = "Error adding user:"
    GET_ALL_USER_ERROR = "Error fetching users:"
