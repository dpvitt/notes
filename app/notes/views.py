from flask import render_template, url_for, flash, redirect, abort, request
from flask_login import login_required, current_user
from . import notes_route
from .. import db
from .forms import NoteForm, DeleteNote, TagForm, EditForm
from ..models import Note, Tag

def user_logged_in(current_user, note):
    if current_user.id != note.user_id:
        return abort(403)

@notes_route.route('/notes')
@login_required
def notes():
    noteForm = NoteForm()
    tagForm = TagForm()
    deleteNote = DeleteNote()
    noteForm.tag.choices = [(t.id, t.tag) for t in Tag.query.filter(Tag.user_id == current_user.id)]
    notes = Note.query.order_by(Note.timestamp.desc()).filter(Note.user_id == current_user.id)
    return render_template('notes/notes.html', noteForm=noteForm, tagForm=tagForm, deleteNote=deleteNote, notes=notes)

@notes_route.route('/add-note/', methods=['POST'])
def add_note():
    body = request.form['body']
    if body:
        tag = Tag.query.filter(Tag.id == request.form['tag']).first()
        note = Note(body=body, user=current_user._get_current_object(), tag=tag)
        db.session.add(note)
    return redirect(url_for('notes_route.notes'))

@notes_route.route('/add-tag/', methods=['POST'])
def add_tag():
    data = request.form['tag']
    if data:
        tag = Tag(tag=data, user=current_user._get_current_object())
        db.session.add(tag)
    return redirect(url_for('notes_route.notes'))

@notes_route.route('/note/<int:id>')
@login_required
def note(id):
    note = Note.query.get_or_404(id)
    user_logged_in(current_user, note)
    return render_template('notes/note.html', note=note)

@notes_route.route('/edit-note/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    note = Note.query.get_or_404(id)
    user_logged_in(current_user, note)
    noteForm = EditForm()
    if noteForm.validate_on_submit():
        note.body = noteForm.body.data
        db.session.add(note)
        flash('Note updated')
        return redirect(url_for('notes_route.note', id=note.id))
    noteForm.body.data = note.body
    return render_template('notes/edit-note.html', noteForm=noteForm)

@notes_route.route('/delete-note/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_note(id):
    user_logged_in(current_user, Note.query.get_or_404(id))
    deleteNote = DeleteNote()
    if deleteNote.validate_on_submit():
        Note.query.filter(Note.id == id).delete()
        db.session.commit()
        return redirect(url_for('notes_route.notes'))
    return render_template('notes/delete-note.html', deleteNote=deleteNote)
