"""
OMDb response with a data structure like this:

{
  "Title": "Titanic",
  "Year": "1997",
  "Rated": "PG-13",
  "Released": "19 Dec 1997",
  "Runtime": "194 min",
  "Genre": "Drama, Romance",
  "Director": "James Cameron",
  "Writer": "James Cameron",
  "Actors": "Leonardo DiCaprio, Kate Winslet, Billy Zane",
  "Plot": "A seventeen-year-old aristocrat falls in love with a kind but
            poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
  "Language": "English, Swedish, Italian, French",
  "Country": "United States",
  "Awards": "Won 11 Oscars. 126 wins & 84 nominations total",
  "Poster": "https://m.media-amazon.com/images/M/
            MV5BYzYyN2FiZmUtYWYzMy00MzViLWJkZTMtOGY1ZjgzNWMwN2YxXkEyXkFqcGc@._V1_SX300.jpg",
  "Ratings": [
    {
      "Source": "Internet Movie Database",
      "Value": "8.0/10"
    },
    {
      "Source": "Rotten Tomatoes",
      "Value": "88%"
    },
    {
      "Source": "Metacritic",
      "Value": "75/100"
    }
  ],
  "Metascore": "75",
  "imdbRating": "8.0",
  "imdbVotes": "1,378,313",
  "imdbID": "tt0120338",
  "Type": "movie",
  "DVD": "N/A",
  "BoxOffice": "$674,354,882",
  "Production": "N/A",
  "Website": "N/A",
  "Response": "True"
}
"""

import requests
from flask import current_app



class OMDbAPI:
    """
    Handles communication with the OMDb API.
    """
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url


    def _make_api_request(self, params: dict) -> tuple[bool, dict | str]:
        """
        Internal helper to handle the technical details of the OMDb API call.
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

    def get_movie_by_title_and_year(self, title: str, year: int = None) -> tuple[bool, dict | str]:
        """
        Fetches detailed movie data from OMDb API by title and year.

        Args:
            title (str): The exact title of the movie.
            year (int): The release year.

        Returns:
            tuple[bool, dict | str]: (True, data_dict) on success,
                                     (False, error_message) on failure.
        """
        return self._make_api_request({
            't': title,
            'y': year
        })


    def search_movie_title(self, title: str) -> tuple[bool, dict | str]:
        """
        Searches the OMDb database for movies matching a partial title.

        Unlike a direct title lookup, this function returns a list of potential
        matches. It is used to provide the user with a selection of movies
        to choose from.

        Args:
            title (str): The search term or partial movie title.

        Returns:
            tuple[bool, dict | str]:
                - Success (True) and a dictionary containing the 'Search' list.
                - Failure (False) and an error message string.
        """
        return self._make_api_request({
            's': title,
            'type': 'movie'
        })

    def get_movie_by_id(self, imdb_id: str) -> tuple[bool, dict | str]:
        """
        Fetches detailed movie information from the OMDb API by its IMDb ID.

        Args:
            imdb_id (str): The unique IMDb identifier for the requested movie.

        Returns:
            tuple[bool, dict | str]:
                - A tuple where the first element indicates success (True/False).
                - The second element is a dictionary with movie details if
                  successful, or an error message string if the request fails.
        """
        return self._make_api_request({
            'i': imdb_id,
            'plot': 'full'
        })
