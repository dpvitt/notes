import unittest
from flask import url_for
from app import create_app, db
from app.models import User

valid_user = {
    'email': 'wiley@example.com',
    'username': 'wiley',
    'password': 'cat',
    'password2': 'cat'
}

invalid_user = {
    'email': 'skepta@example.com',
    'username': 'skepta',
    'password': 'cat',
    'password2': 'dog'
}

class AuthTestCase(unittest.TestCase):

    ##### Setup #####

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    ##### Test Cases #####

    def test_auth_can_register(self):
        response = self.client.post(url_for('auth_route.register'), data=valid_user)
        self.assertTrue(response.status_code == 302)
        self.assertTrue(User.query.filter(User.username == 'wiley'))

    def test_auth_cannot_register(self):
        response = self.client.post(url_for('auth_route.register'), data=invalid_user)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(User.query.all()) == 0)

    def test_auth_duplicate_registration(self):
        response = self.client.post(url_for('auth_route.register'), data=valid_user)
        response = self.client.post(url_for('auth_route.register'), data=valid_user)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(User.query.all()) == 1)
