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
    @api.expect(text_request)
    @api.marshal_list_with(entity_response)
    def post(self):
        content = request.json.get("text")
        return extract(content)


@entities.route("/url")
class Url(Resource):
    @require_auth
    @api.doc(
        responses={200: "Success", 401: "Unauthorized"},
        params={"API_KEY": {"in": "header"}},
    )
    @api.expect(url_request)
    @api.marshal_list_with(entity_response)
    def post(self):
        url = request.json.get("url")
        content = scrape(url)
        return extract(content)


artist = api.namespace(
    "artist", description="extract an artist from plain text or a url"
)

artist_text_request = api.model("Text Request", {"text": fields.String(required=True)})

artist_url_request = api.model("URL Request", {"url": fields.String(required=True)})

popularity = api.model("Popularity", {"dsp": fields.String, "value": fields.Integer})

artist_response = api.model(
    "Artist Response",
    {
        "name": fields.String,
        "popularity": fields.List(fields.Nested(popularity)),
        "metafireId": fields.String,
    },
)


def metafire(entities: List[Dict]) -> Dict:
    metafire = met.Metafire()
    for e in entities:
        artists = metafire.find_artist(e["text"])
        if not [a for a in artists if a["popularity"]]:
            continue
        return sorted(
            [a for a in artists if a["popularity"]],
            key=lambda x: x["popularity"][0]["value"],
        )[-1]
    return {}


@artist.route("/text")
class ArtistText(Resource):
    @require_auth
    @api.doc(
        responses={200: "Success", 401: "Unauthorized"},
        params={"API_KEY": {"in": "header"}},
    )
    @api.expect(artist_text_request)
    @api.marshal_with(artist_response)
    def post(self):
        content = request.json.get("text")
        entities = extract(content)
        artist = metafire(entities)

        if not artist:
            abort(404, "No artist found")

        return {
            "name": artist["name"],
            "popularity": artist["popularity"],
            "metafireId": artist["metafireId"],
        }


@artist.route("/url")
class ArtistUrl(Resource):
    @require_auth
    @api.doc(
        responses={200: "Success", 401: "Unauthorized"},
        params={"API_KEY": {"in": "header"}},
    )
    @api.expect(artist_url_request)
    @api.marshal_with(artist_response)
    def post(self):
        url = request.json.get("url")
        content = scrape(url)
        entities = extract(content)
        artist = metafire(entities)

        if not artist:
            abort(404, "No artist found")

        return {
            "name": artist["name"],
            "popularity": artist["popularity"],
            "metafireId": artist["metafireId"],
        }
