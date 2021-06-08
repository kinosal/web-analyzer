"""Endpoints for API v1."""

# Import from standard library
from typing import List, Dict

# Import from 3rd party libraries
from flask import request, abort
from flask_restx import Api, Resource, fields

# Import modules
from app.api import require_auth
from app.api.v1 import api_v1
import app.scripts.comprehend as com
import app.scripts.scrape as scr
import app.scripts.metafire as met
import app.scripts.spotify as spo

api = Api(
    api_v1,
    version="1.0",
    title="Web Analyzer (Scalable Scraper) API",
    description="Detecting entities from web pages",
)

entities = api.namespace(
    "entities", description="extract entities from plain text or a url"
)

text_request = api.model("Text Request", {"text": fields.String(required=True)})

url_request = api.model("URL Request", {"url": fields.String(required=True)})

entity_response = api.model(
    "Entity Response",
    {"type": fields.String, "text": fields.String, "count": fields.Integer},
)


def scrape(url: str) -> str:
    scraper = scr.Scraper()
    response = scraper.request_url(url)
    return scraper.extract_content(response)


def extract(content: str) -> List[Dict]:
    comprehender = com.Comprehend()
    language = comprehender.language(content[:2500])
    return comprehender.entities(content[:2500], language)


@entities.route("/text")
class Text(Resource):
    @require_auth
    @api.doc(
        responses={200: "Success", 401: "Unauthorized"},
        params={"API_KEY": {"in": "header"}},
    )
    @api.expect(text_request, validate=True)
    @api.marshal_list_with(entity_response)
    def post(self):
        return extract(request.json["text"])


@entities.route("/url")
class Url(Resource):
    @require_auth
    @api.doc(
        responses={200: "Success", 401: "Unauthorized"},
        params={"API_KEY": {"in": "header"}},
    )
    @api.expect(url_request, validate=True)
    @api.marshal_list_with(entity_response)
    def post(self):
        content = scrape(request.json["url"])
        return extract(content)


artist = api.namespace(
    "artist", description="extract an artist from plain text or a url"
)

artist_text_request = api.model(
    "Artist Text Request",
    {
        "text": fields.String(required=True),
        "search": fields.String(enum=["metafire", "spotify"], default="metafire"),
    },
)

artist_url_request = api.model(
    "Artist URL Request",
    {
        "url": fields.String(required=True),
        "search": fields.String(enum=["metafire", "spotify"], default="metafire"),
    },
)

artist_response = api.model(
    "Artist Response",
    {
        "name": fields.String,
        "popularity": fields.Integer,
        "external_id": fields.String,
    },
)


def metafire(entities: List[Dict], require_popularity: bool = False) -> Dict:
    metafire = met.Metafire()

    for e in entities:
        artists = metafire.find_artists(e["text"])
        if not artists:
            continue

        if require_popularity:
            artists = [a for a in artists if a["popularity"]]
            if not artists:
                continue
            artists = sorted(
                artists, key=lambda x: x["popularity"][0]["value"], reverse=True
            )

        print(artists, "\n")  # TODO: Remove after testing

        return {
            "name": artists[0]["name"],
            "popularity": (
                artists[0]["popularity"][0]["value"]
                if artists[0]["popularity"] else None
            ),
            "external_id": artists[0]["metafireId"],
        }
    return {}


def spotify(entities: List[Dict]) -> Dict:
    spotify = spo.Spotify()

    for e in entities:
        artists = spotify.find_artists(e["text"])
        if not artists:
            continue

        print(artists, "\n")  # TODO: Remove after testing

        return {
            "name": artists[0]["name"],
            "popularity": artists[0]["popularity"],
            "external_id": artists[0]["id"],
        }
    return {}


@artist.route("/text")
class ArtistText(Resource):
    @require_auth
    @api.doc(
        responses={200: "Success", 401: "Unauthorized"},
        params={"API_KEY": {"in": "header"}},
    )
    @api.expect(artist_text_request, validate=True)
    @api.marshal_with(artist_response)
    def post(self):
        entities = extract(request.json["text"])

        print(entities, "\n")  # TODO: Remove after testing

        if request.json["search"] == "metafire":
            artist = metafire(entities)
        elif request.json["search"] == "spotify":
            artist = spotify(entities)

        if not artist:
            abort(404, "No artist found")

        return artist


@artist.route("/url")
class ArtistUrl(Resource):
    @require_auth
    @api.doc(
        responses={200: "Success", 401: "Unauthorized"},
        params={"API_KEY": {"in": "header"}},
    )
    @api.expect(artist_url_request, validate=True)
    @api.marshal_with(artist_response)
    def post(self):
        content = scrape(request.json["url"])
        entities = extract(content)

        print(entities, "\n")  # TODO: Remove after testing

        if request.json["search"] == "metafire":
            artist = metafire(entities)
        elif request.json["search"] == "spotify":
            artist = spotify(entities)

        if not artist:
            abort(404, "No artist found")

        return artist
