"""Metafire connectors."""

# Import from standard library
from typing import List, Dict
import requests


class Metafire:
    """Controller for requests to the Metafire Search API."""

    api_url = "https://data-api-prod.metafire.co/api/Search"

    def find_artists(
        self, search_key: str, limit: int = 10, accuracy: int = 90
    ) -> List[Dict]:
        """Search Metafire for artist from query string."""
        response = requests.get(
            f"{self.api_url}?DataType=artists&Limit={limit}"
            f"&MinimumMatchingScore={accuracy}&Search={search_key}"
        )
        return response.json()["data"]
