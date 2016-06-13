import unittest, test_auth_mocks
from flask import url_for
from app import create_app, db
from app.models import User

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

    ##### Register Cases #####

    def test_auth_can_register(self):
        response = self.client.post(url_for('auth_route.register'), data=test_auth_mocks.register_valid_user)
        self.assertTrue(response.status_code == 302)
        self.assertTrue(User.query.filter(User.username == 'wiley'))

    def test_auth_cannot_register(self):
        response = self.client.post(url_for('auth_route.register'), data=test_auth_mocks.register_invalid_user)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(User.query.all()) == 0)

    def test_auth_duplicate_registration(self):
        response = self.client.post(url_for('auth_route.register'), data=test_auth_mocks.register_valid_user)
        response = self.client.post(url_for('auth_route.register'), data=test_auth_mocks.register_valid_user)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(User.query.all()) == 1)
        self.assertTrue('Email already registered' in response.get_data(as_text=True))
        self.assertTrue('Username already in use' in response.get_data(as_text=True))

    ##### Login Cases #####

    def test_auth_can_login(self):
        self.client.post(url_for('auth_route.register'), data=test_auth_mocks.register_valid_user)
        response = self.client.post(url_for('auth_route.login'), data=test_auth_mocks.login_valid_user)
        self.assertTrue(response.status_code == 302)
        self.assertTrue('/notes' in response.get_data(as_text=True))

    def test_auth_cannot_login(self):
        response = self.client.post(url_for('auth_route.login'), data=test_auth_mocks.login_invalid_user)
        self.assertTrue(response.status_code == 200)
        self.assertTrue('Invalid username or password' in response.get_data(as_text=True))

    def test_auth_cannot_login_required(self):
        response = self.client.post(url_for('auth_route.login'), data=test_auth_mocks.login_empty_user)
        self.assertTrue(response.status_code == 200)
        self.assertTrue('This field is required' in response.get_data(as_text=True))

    ##### Logout Cases #####

    def test_auth_can_logout(self):
        self.client.post(url_for('auth_route.register'), data=test_auth_mocks.register_valid_user)
        self.client.post(url_for('auth_route.login'), data=test_auth_mocks.login_valid_user)
        response = self.client.get(url_for('auth_route.logout'))
        self.assertTrue(response.status_code == 302)
        self.assertTrue('/login' in response.get_data(as_text=True))
