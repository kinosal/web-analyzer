"""Metafire connectors."""

# Import from standard library
from typing import List, Dict
import requests

# Import third party libraries
from fuzzywuzzy import fuzz


class Metafire:
    """Controller for requests to the Metafire Search API."""

    api_url = "https://data-api-prod.metafire.co/api/Search"

    def find_artists(
        self,
        search_key: str,
        limit: int = 10,
        accuracy: int = 90,
        score: bool = True,
    ) -> List[Dict]:
        """Search Metafire for artist from query string."""
        artists = requests.get(
            f"{self.api_url}?DataType=artists&Limit={limit}"
            f"&MinimumMatchingScore={accuracy}&Search={search_key}"
        ).json()["data"]

        if not artists:
            return []

        if score:
            artists = sorted(
                [a for a in artists if a["popularity"] and a["popularity"][0]["value"] > 0],
                key=lambda a: (
                    (len(artists) - artists.index(a)) * 100/len(artists)
                    + a["popularity"][0]["value"]
                    + fuzz.ratio(search_key, a["name"]) * 2
                ),
                reverse=True,
            )

        return [
            {
                "name": a["name"],
                "popularity": (
                    a["popularity"][0]["value"]
                    if a["popularity"] else None
                ),
                "external_id": a["metafireId"],
            }
            for a in artists
        ]
