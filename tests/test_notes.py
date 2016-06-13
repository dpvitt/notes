import unittest, test_mocks
from flask import url_for
from app import create_app, db
from app.models import Note
from test_auth import AuthTestCase

class NoteTestCase(unittest.TestCase):

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

    ##### Notes Cases #####

    def test_notes_view_notes(self):
        AuthTestCase.signInUser(self)
        response = self.client.get(url_for('notes_route.notes'))
        self.assertTrue(response.status_code == 200)
        self.assertTrue("wiley's notes" in response.get_data(as_text=True))
        self.assertTrue('name="body"' in response.get_data(as_text=True))

    def test_notes_can_add_note(self):
        AuthTestCase.signInUser(self)
        response = self.client.post(url_for('notes_route.notes'), data=test_mocks.note_body)
        self.assertTrue(response.status_code == 200)
        self.assertTrue('this is an example note' in response.get_data(as_text=True))

    def test_notes_cannot_add_note(self):
        AuthTestCase.signInUser(self)
        response = self.client.post(url_for('notes_route.notes'), data=test_mocks.note_empty)
        self.assertTrue(response.status_code == 200)
        self.assertTrue('This field is required.' in response.get_data(as_text=True))
