import os
import unittest
import json
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)

from app import create_app, db
from app.config import TestingConfig
from app.models.models import User


class TestSetup(unittest.TestCase):
    def setUp(self):
        """
        Create new app and database for each test
        """
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        Remove databse and app context after each test
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_root(self):
        """
        Test that app root responds properly
        """
        response = self.app.test_client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_ping(self):
        """
        Test that app can be pinged wth GET and POST
        """
        response = self.app.test_client().get('/ping')
        self.assertEqual(response.status_code, 200)
        response = self.app.test_client().post('/ping')
        self.assertEqual(response.status_code, 200)


class TestUser(TestSetup):
    def test_creation(self):
        """
        Add a user to the database
        """
        self.assertEqual(User.query.count(), 0)
        db.session.add(User())
        db.session.commit()
        self.assertEqual(User.query.count(), 1)

    def test_users_route(self):
        """
        Get user count from /users
        """
        response = self.app.test_client().get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn('0 entries in DB', str(response.data))

    def test_user_route(self):
        """
        Get single user with id from /user/<id>
        """
        db.session.add(User())
        db.session.commit()
        response = self.app.test_client().get('/users/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['id'], 1)

    def test_error(self):
        """
        Return error response for missing user
        """
        response = self.app.test_client().get('/users/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['code'], 404)


if __name__ == '__main__':
    unittest.main()
