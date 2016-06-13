from flask import render_template, url_for, flash, redirect, abort
from flask_login import login_required, current_user
from . import notes_route
from .. import db
from .forms import NoteForm, DeleteNote
from ..models import Note

@notes_route.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    noteForm = NoteForm()
    if noteForm.validate_on_submit():
        note = Note(body=noteForm.body.data, author=current_user._get_current_object())
        db.session.add(note)
    notes = Note.query.order_by(Note.timestamp.desc()).filter(Note.author_id == current_user.id)
    return render_template('notes/notes.html', noteForm=noteForm, notes=notes)

@notes_route.route('/note/<int:id>')
@login_required
def note(id):
    note = Note.query.get_or_404(id)
    if current_user.id != note.author_id:
        abort(403)
    return render_template('notes/note.html', note=note)

@notes_route.route('/edit-note/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    note = Note.query.get_or_404(id)
    if current_user.id != note.author_id:
        abort(403)
    noteForm = NoteForm()
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
    note = Note.query.get_or_404(id)
    if current_user.id != note.author_id:
        abort(403)
    deleteNote = DeleteNote()
    if deleteNote.validate_on_submit():
        Note.query.filter(Note.id == id).delete()
        db.session.commit()
        return redirect(url_for('notes_route.notes'))
    return render_template('notes/delete-note.html', deleteNote=deleteNote)
