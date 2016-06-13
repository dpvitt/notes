import unittest
from flask import current_app, url_for
from app import create_app

class MainRouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()

    def test_main_route(self):
        reponse = self.client.get(url_for('main_route.index'))
        self.assertTrue('hi' in reponse.get_data(as_text=True))
