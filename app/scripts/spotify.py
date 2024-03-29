"""Spotify connectors."""

# Import from standard library
import os
import requests
from typing import List, Dict

# Import third party libraries
from thefuzz import fuzz

class Spotify:
    """Controller for requests to the Spotify Public API."""

    def __init__(self, client_id=None, client_secret=None):
        self.client_id = client_id or os.environ["SPOTIFY_CLIENT_ID"]
        self.client_secret = client_secret or os.environ["SPOTIFY_CLIENT_SECRET"]
        self.auth_token = self.get_auth_token()
        self.api_url = "https://api.spotify.com/v1/"

    def get_auth_token(self) -> str:
        """Get authorization token."""
        auth_response = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )
        return auth_response.json()["access_token"]

    def find_artists(
        self,
        search_key: str,
        score: bool = True,
    ) -> List[Dict]:
        """Search Spotify API."""
        artists = requests.get(
            f"{self.api_url}search?q=artist:{search_key}&type=artist",
            headers={"Authorization": f"Bearer {self.auth_token}"},
        ).json()["artists"]["items"]

        if not artists:
            return []

        if score:
            artists = sorted(
                [a for a in artists if a["popularity"] > 0],
                key=lambda a: (
                    (len(artists) - artists.index(a)) * 100/len(artists)
                    + a["popularity"]
                    + fuzz.ratio(search_key, a["name"])
                ),
                reverse=True,
            )

        return [
            {
                "name": a["name"],
                "popularity": a["popularity"],
                "external_id": a["id"],
            }
            for a in artists
        ]
