"""Metafire connectors."""

# Import from standard library
from typing import List, Dict
import requests


class Metafire:
    """Controller for requests to the Metafire Search API."""

    api_url = "https://data-api-prod.metafire.co/api/Search"

    def find_artists(
        self,
        search_key: str,
        limit: int = 10,
        accuracy: int = 90,
        require_popularity: bool = False,
    ) -> List[Dict]:
        """Search Metafire for artist from query string."""
        artists = requests.get(
            f"{self.api_url}?DataType=artists&Limit={limit}"
            f"&MinimumMatchingScore={accuracy}&Search={search_key}"
        ).json()["data"]

        if not artists:
            return []

        if require_popularity:
            artists = [
                a for a in artists
                if a["popularity"] and a["popularity"][0]["value"] > 0
            ]
            if not artists:
                return []

            # artists = sorted(
            #     artists, key=lambda a: a["popularity"][0]["value"], reverse=True
            # )

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
