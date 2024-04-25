"""Endpoints for API v1."""

# Import from standard library
from typing import List, Dict
import re

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

from app.models.models import Url as UrlModel
from app.models.models import save_url

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
    language = comprehender.language(content)
    return comprehender.entities(content, language)


@entities.route("/text")
class Text(Resource):
    @require_auth
    @api.doc(
        responses={200: "Success", 401: "Unauthorized"},
        params={"x-api-key": {"in": "header"}},
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
        params={"x-api-key": {"in": "header"}},
    )
    @api.expect(url_request, validate=True)
    @api.marshal_list_with(entity_response)
    def post(self):
        content = scrape(request.json["url"])
        url_text = " ".join(
            re.split('/|-|_', request.json["url"].strip("https://"))
        )
        return extract(url_text + " " + content)


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
        "force_rescan": fields.Boolean(default=False),
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


def find(entities: List[Dict], source: str) -> List[Dict]:
    if source == "metafire":
        finder = met.Metafire()
    if source == "spotify":
        finder = spo.Spotify()

    for e in entities:
        artists = finder.find_artists(e["text"], score=True)
        if not artists:
            continue

        print(artists, "\n")  # TODO: Remove after testing
        return artists
    return []


@artist.route("/text")
class ArtistText(Resource):
    @require_auth
    @api.doc(
        responses={200: "Success", 401: "Unauthorized"},
        params={"x-api-key": {"in": "header"}},
    )
    @api.expect(artist_text_request, validate=True)
    @api.marshal_with(artist_response)
    def post(self):
        entities = extract(request.json["text"])
        print(entities, "\n")  # TODO: Remove after testing
        artists = find(entities, request.json["search"])
        if not artists:
            abort(404, "No artist found")
        return artists[0]


@artist.route("/url")
class ArtistUrl(Resource):
    @require_auth
    @api.doc(
        responses={200: "Success", 401: "Unauthorized"},
        params={"x-api-key": {"in": "header"}},
    )
    @api.expect(artist_url_request, validate=True)
    @api.marshal_with(artist_response)
    def post(self):
        if not request.json["force_rescan"]:
            url_model = UrlModel.query.filter(
                UrlModel.url == request.json["url"]
            ).first()
            if url_model:
                return {
                    "name": url_model.artist_name,
                    "popularity": url_model.popularity,
                    "external_id": url_model.external_id,
                }

        content = scrape(request.json["url"])
        path = " ".join(
            re.split('/|-|_', request.json["url"])[3:]
        )
        entities = extract(path + " " + content)
        print(entities, "\n")  # TODO: Remove after testing

        artists = find(entities, request.json["search"])

        if not artists:
            abort(404, "No artist found")

        # TODO: Connect to database
        # save_url(
        #     request.json["url"],
        #     content,
        #     entities,
        #     artists,
        #     request.json["search"],
        # )

        return artists[0]
