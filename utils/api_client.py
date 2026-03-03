import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

class KinopoiskAPIClient:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"X-API-KEY": api_key})
        self._setup_retry_strategy()

    def _setup_retry_strategy(self):
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _make_request(self, endpoint: str, params: dict = None) -> dict:
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response: {response.text}")
            raise
        except Exception as e:
            print(f"Request failed: {e}")
            raise

    def get_film_details_by_id(self, film_id: int) -> dict:
        endpoint = f"api/v2.2/films/{film_id}"
        return self._make_request(endpoint)

    def get_premieres_list(self, year: int, month: str = "JANUARY"):
        endpoint = "/api/v2.2/films/premieres"
        params = {
            "year": year,
            "month": month
        }
        return self._make_request(endpoint, params)

    def get_similar_films(self, film_id: int) -> dict:
        endpoint = f"api/v2.2/films/{film_id}/similars"
        return self._make_request(endpoint)

    def get_films_by_filters(self, **filters) -> dict:
        valid_filters = {k: v for k, v in filters.items() if k in ["genre", "year", "ratingFrom", "order"]}
        endpoint = "api/v2.2/films"
        return self._make_request(endpoint, valid_filters)

    def get_seasons_data(self, series_id: int) -> dict:
        endpoint = f"api/v2.2/films/{series_id}/seasons"
        return self._make_request(endpoint)
