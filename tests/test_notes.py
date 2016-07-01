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

    def test_notes_view_by_tag(self):
        AuthTestCase.signInUser(self)
        self.client.post(url_for('notes_route.add_tag'), data=test_mocks.tag_body)
        self.client.post(url_for('notes_route.add_tag'), data=test_mocks.tag_body_2)
        self.client.post(url_for('notes_route.add_note'), data=test_mocks.note_body)
        self.client.post(url_for('notes_route.add_note'), data=test_mocks.note_body_2)
        notes = self.client.get(url_for('notes_route.notes_by_tag', id=1))
        self.assertTrue('this is an example note' in notes.get_data(as_text=True))
        self.assertFalse('another note' in notes.get_data(as_text=True))

    def test_notes_can_add_note(self):
        AuthTestCase.signInUser(self)
        self.client.post(url_for('notes_route.add_tag'), data=test_mocks.tag_body)
        response = self.client.post(url_for('notes_route.add_note'), data=test_mocks.note_body)
        self.assertTrue(response.status_code == 302)
        notes = self.client.get(url_for('notes_route.notes'))
        self.assertTrue('this is an example note' in notes.get_data(as_text=True))

    def test_notes_can_add_tag(self):
        AuthTestCase.signInUser(self)
        response = self.client.post(url_for('notes_route.add_tag'), data=test_mocks.tag_body)
        self.assertTrue(response.status_code == 302)
        notes = self.client.get(url_for('notes_route.notes'))
        self.assertTrue('cheese' in notes.get_data(as_text=True))

    def test_notes_view_note(self):
        AuthTestCase.signInUser(self)
        self.client.post(url_for('notes_route.add_tag'), data=test_mocks.tag_body)
        self.client.post(url_for('notes_route.add_note'), data=test_mocks.note_body)
        response = self.client.get(url_for('notes_route.note', id=1))
        self.assertTrue(response.status_code == 200)
        self.assertTrue('<p>this is an example note</p>' in response.get_data(as_text=True))

    def test_notes_cannot_view_public_note(self):
        AuthTestCase.signInUser(self)
        self.client.post(url_for('notes_route.add_tag'), data=test_mocks.tag_body)
        self.client.post(url_for('notes_route.add_note'), data=test_mocks.note_body_public)
        self.client.get(url_for('auth_route.logout'))
        response = self.client.get(url_for('notes_route.note', id=1))
        self.assertTrue(response.status_code == 200)

    def test_notes_cannot_view_private_note(self):
        AuthTestCase.signInUser(self)
        self.client.post(url_for('notes_route.add_tag'), data=test_mocks.tag_body)
        self.client.post(url_for('notes_route.add_note'), data=test_mocks.note_body)
        self.client.get(url_for('auth_route.logout'))
        response = self.client.get(url_for('notes_route.note', id=1))
        self.assertTrue(response.status_code == 403)
        self.assertTrue('forbidden' in response.get_data(as_text=True))

    def test_notes_edit_note_content(self):
        AuthTestCase.signInUser(self)
        self.client.post(url_for('notes_route.add_tag'), data=test_mocks.tag_body)
        self.client.post(url_for('notes_route.add_note'), data=test_mocks.note_body)
        response = self.client.get(url_for('notes_route.edit_note', id=1))
        self.assertTrue(response.status_code == 200)
        self.assertTrue('this is an example note</textarea>' in response.get_data(as_text=True))

    def test_notes_edit_note_post(self):
        AuthTestCase.signInUser(self)
        self.client.post(url_for('notes_route.add_tag'), data=test_mocks.tag_body)
        self.client.post(url_for('notes_route.add_note'), data=test_mocks.note_body)
        edit = self.client.post(url_for('notes_route.edit_note', id=1), data=test_mocks.note_updated_body)
        self.assertTrue(edit.status_code == 302)
        response = self.client.get(url_for('notes_route.note', id=1))
        self.assertTrue('this is an updated note' in response.get_data(as_text=True))

    def test_notes_delete_note(self):
        AuthTestCase.signInUser(self)
        self.client.post(url_for('notes_route.add_note'), data=test_mocks.note_body)
        delete = self.client.post(url_for('notes_route.delete_note', id=1))
        self.assertTrue(delete.status_code == 302)
        response = self.client.get(url_for('notes_route.note', id=1))
        self.assertTrue(response.status_code == 404)
