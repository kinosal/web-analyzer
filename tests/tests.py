import os
import unittest

import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
print(BASE_DIR)
sys.path.insert(0, BASE_DIR)

from app import create_app, db
from app.config import Config
from app.models.models import Campaign


class TestConfig(Config):
    TESTING = True
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')


class TestSetup(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_root(self):
        response = self.app.test_client().get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
