"""
omdb_api.py – Client interface for the Open Movie Database (OMDb) API.

This module provides a Pythonic wrapper around the OMDb API, abstracting the
complexities of HTTP requests, authentication, and error handling. It offers
two primary methods for retrieving movie data: searching by title and fetching
by IMDb ID, both with built-in validation and standardized response formats.

Key Features:
-------------
- **Simplified API Access**: Encapsulates HTTP requests and parameter handling.
- **Error Resilience**: Converts network/API errors into user-friendly messages.
- **Response Standardization**: Returns consistent tuple-based responses (success, data/error).
- **Timeout Handling**: Implements a 5-second timeout for all API requests.
- **Type Safety**: Uses Python type hints for better code clarity and IDE support.

Supported Operations:
---------------------
1. **Movie Lookup by ID**: Retrieve complete metadata for a specific movie using its IMDb ID.
2. **Title Search**: Perform fuzzy searches for movies by title, restricted to movie-type results.

Error Handling:
---------------
All methods return tuples of (success: bool, result: Union[dict, str]) where:
- success: Boolean indicating if the operation completed successfully
- result: Either:
  - A dictionary of movie data (on success)
  - A user-friendly error message string (on failure)

Handled Error Cases:
- Network timeouts and connection issues
- HTTP errors (4xx/5xx responses)
- Invalid API keys or rate limiting
- Missing/invalid movie data
- JSON parsing errors

Configuration:
--------------
Requires an API key from OMDb (free tier available at http://www.omdbapi.com/)
and the base API URL (typically 'http://www.omdbapi.com/').
"""
import requests


class OMDbAPI:
    """
    A service client for the OMDb (Open Movie Database) API.

    This class encapsulates the technical logic for communicating with the OMDb
    API service. It handles authentication via API keys, simplifies common
    query patterns (search by title vs. lookup by ID), and provides a
    standardized error handling layer to convert network or API exceptions
    into user-friendly messages.
    """
    def __init__(self, api_key: str, base_url: str):
        """
        Initializes the OMDbAPI service with credentials and endpoint details.

        Args:
            api_key (str): The secret API key required for authenticating
                requests with OMDb.
            base_url (str): The root URL of the OMDb API service
                (e.g., 'http://www.omdbapi.com/').
        """
        self.api_key = api_key
        self.base_url = base_url


    def get_movie_by_id(self, imdb_id: str) -> tuple[bool, dict | str]:
        """
        Fetches full movie details from the OMDb API using a specific IMDb ID.

        This method requests the 'full' plot version of the movie metadata
        to ensure all available information is retrieved.

        Args:
            imdb_id (str): The unique IMDb identifier (e.g., 'tt0111161')
                for the requested movie.

        Returns:
            tuple[bool, dict | str]:
                - (True, movie_details_dict) if the movie was found and
                  the API returned a successful response.
                - (False, error_message) if the movie ID is invalid, the
                  API is unreachable, or the OMDb response contains an error.
        """
        return self._make_api_request({
            'i': imdb_id,
            'plot': 'full'
        })


    def search_movie_title(self, title: str) -> tuple[bool, dict | str]:
        """
        Searches the OMDb database for movies matching a search term.

        This method performs a fuzzy search and returns a collection of
        potential matches. It is specifically restricted to entries of
        type 'movie' to ensure relevance for the collection.

        Args:
            title (str): The search query or partial movie title
                (e.g., 'Inception').

        Returns:
            tuple[bool, dict | str]:
                - (True, results_dict): A dictionary where the 'Search' key
                  contains a list of abbreviated movie objects.
                - (False, error_message): If no movies were found or the
                  API request encountered an error.
        """
        return self._make_api_request({
            's': title,
            'type': 'movie'
        })


    def _make_api_request(self, params: dict) -> tuple[bool, dict | str]:
        """
        Internal helper to handle the technical details of the OMDb API call.

        This method centralizes the HTTP communication, injects the API key,
        and provides robust error handling for network issues and API-specific
        error responses.

        Args:
            params (dict): Query parameters for the OMDb API (e.g., 's' or 'i').
                The 'apikey' is automatically appended to these parameters.

        Returns:
            tuple[bool, dict | str]:
                - (True, data): On success, where 'data' is the parsed JSON
                  dictionary from OMDb.
                - (False, message): On failure, returning a user-friendly error
                  message (either from the API or a custom network error).

        Raises:
            Note: While 'requests' exceptions are caught internally
        """
        params['apikey'] = self.api_key
        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=5)
            response.raise_for_status()
            data = response.json()

            if data.get("Response") == 'True':
                return True, data
            return False, data.get('Error',"Unknown API Error")

        except requests.exceptions.Timeout:
            return False, "The request timed out. Please try again later."
        except requests.exceptions.ConnectionError:
            return False, "Network error. Check your internet connection."
        except requests.exceptions.HTTPError as http_err:
            return False, f"HTTP error occurred: {http_err}"
        except requests.exceptions.RequestException as error:
            return False, f"An unexpected error occurred: {error}"
