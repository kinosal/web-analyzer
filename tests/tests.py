"""Unit tests."""

import json
from os import environ
import unittest

from app.config import TestingConfig
from app import create_app
from app import db
from app.models.models import User


class TestSetup(unittest.TestCase):
    """Basic unit testing setup and default tests."""

    def setUp(self):
        """Create new app and database for each test."""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Remove databse and app context after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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
        response = self.app.test_client().get("/protected", headers={"API_KEY": key})
        self.assertEqual(response.status_code, 401)

        key = environ.get("API_KEY")
        response = self.app.test_client().get("/protected", headers={"API_KEY": key})
        self.assertEqual(response.status_code, 200)

        secure_origin = environ.get("SECURE_ORIGINS").split(",")[0]
        response = self.app.test_client().get(
            "/protected", headers={"Origin": secure_origin}
        )
        self.assertEqual(response.status_code, 200)


class TestUser(TestSetup):
    """Tests for user model and respective routes."""

    def test_creation(self):
        """Add a user to the database."""
        self.assertEqual(User.query.count(), 0)
        db.session.add(User())
        db.session.commit()
        self.assertEqual(User.query.count(), 1)

    def test_users_route(self):
        """Get user count from API v1."""
        key = environ.get("API_KEY")
        response = self.app.test_client().get("/v1/users", headers={"API_KEY": key})
        self.assertEqual(response.status_code, 200)
        self.assertIn("0 entries in DB", str(response.data))

    def test_user_route(self):
        """Get single user with id from API v1."""
        db.session.add(User())
        db.session.commit()
        key = environ.get("API_KEY")
        response = self.app.test_client().get("/v1/users/1", headers={"API_KEY": key})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["id"], 1)

    def test_error(self):
        """Return error response for missing user from API v1."""
        key = environ.get("API_KEY")
        response = self.app.test_client().get("/v1/users/1", headers={"API_KEY": key})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["code"], 404)


if __name__ == "__main__":
    unittest.main()
