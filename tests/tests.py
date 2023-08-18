"""Unit tests."""

import json
from os import environ
import unittest

from app.config import TestingConfig
from app import create_app


class TestSetup(unittest.TestCase):
    """Unit testing setup."""

    def setUp(self):
        """Create new app and database for each test."""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Remove databse and app context after each test."""
        self.app_context.pop()


class TestBasic(TestSetup):
    """Basic default tests."""

    def test_root(self):
        """Test that app root responds properly."""
        response = self.app.test_client().get("/")
        self.assertEqual(response.status_code, 200)

    def test_ping(self):
        """Test that app can be pinged wth GET and POST."""
        response = self.app.test_client().get("/ping")
        self.assertEqual(response.status_code, 200)
        response = self.app.test_client().post("/ping")
        self.assertEqual(response.status_code, 200)

    def test_protected(self):
        """Test that protected resource can be accessed with api key or origin."""
        response = self.app.test_client().get("/protected")
        self.assertEqual(response.status_code, 401)

        key = "bad_key"
        response = self.app.test_client().get("/protected", headers={"x-api-key": key})
        self.assertEqual(response.status_code, 401)

        key = environ.get("API_KEY")
        response = self.app.test_client().get("/protected", headers={"x-api-key": key})
        self.assertEqual(response.status_code, 200)

    def test_error(self):
        """Return error response for missing user from API v1."""
        key = environ.get("API_KEY")
        response = self.app.test_client().get("/error", headers={"x-api-key": key})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["code"], 404)
