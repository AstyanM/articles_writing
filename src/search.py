import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()


class SerperClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("SERPER_API_KEY")
        if not self.api_key:
            # We don't raise error immediately to allow instantiation, but search will fail if not provided.
            # Ideally should verify.
            pass
        self.base_url = "https://google.serper.dev/search"

    def search(self, query: str, date_range: str = None, num_results: int = 10) -> dict:
        """
        Perform a search using Serper.dev API.

        Args:
            query: Search query string.
            date_range: Optional date filter (e.g., 'h', 'd', 'w', 'm', 'y').
            num_results: Number of results to return.

        Returns:
            Dictionary containing search results.
        """
        if not self.api_key:
            raise ValueError(
                "SERPER_API_KEY is not set. Please provide it in constructor or set it in .env file.")

        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

        payload = {
            'q': query,
            'num': num_results,
            'gl': 'fr',
            'hl': 'fr'
        }

        if date_range:
            # Serper uses 'tbs' parameter for time-based search
            # 'qdr' comes from Google's query date range.
            # qdr:h (past hour), qdr:d (past 24h), qdr:w (past week), qdr:m (past month), qdr:y (past year)
            payload['tbs'] = f"qdr:{date_range}"

        try:
            response = requests.post(
                self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during Serper API call: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
            return {}
