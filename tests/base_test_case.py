from flask_testing import TestCase

from app import create_app


class BaseTestCase(TestCase):
    def create_app(self):
        return create_app('app.config.TestingConfig')

    def setUp(self):
        pass

    def tearDown(self):
        pass
