from flask import render_template, url_for, flash, redirect, abort, request
from flask_login import login_required, current_user
from sqlalchemy import extract
from . import notes_route
from .. import db
from .forms import NoteForm, DeleteNote, TagForm, EditForm
from ..helpers import TimeHelper
from ..models import Note, Tag

@notes_route.context_processor
def utility_processor():
    return dict(format_time=TimeHelper.format_time, get_day=TimeHelper.get_day, get_month=TimeHelper.get_month, get_year=TimeHelper.get_year)

def user_logged_in(current_user, note):
    if current_user.id != note.user_id:
        return abort(403)

@notes_route.route('/notes')
@login_required
def notes():
    noteForm = NoteForm()
    noteForm.tag.choices = [(t.id, t.tag) for t in Tag.query.filter(Tag.user_id == current_user.id)]
    notes = Note.query.order_by(Note.timestamp.desc()).filter(Note.user_id == current_user.id)
    return render_template('notes/notes.html', noteForm=noteForm, tagForm=TagForm(), deleteNote=DeleteNote(), notes=notes)

@notes_route.route('/notes/tag/<int:id>')
@login_required
def notes_by_tag(id):
    noteForm = NoteForm()
    noteForm.tag.choices = [(t.id, t.tag) for t in Tag.query.filter(Tag.user_id == current_user.id)]
    notes = Note.query.order_by(Note.timestamp.desc()).filter(Note.tag_id == id).filter(Note.user_id == current_user.id)
    return render_template('notes/notes.html', noteForm=noteForm, tagForm=TagForm(), deleteNote=DeleteNote(), notes=notes)

@notes_route.route('/notes/month/<int:month>/<int:year>')
@login_required
def notes_by_month(year, month):
    noteForm = NoteForm()
    noteForm.tag.choices = [(t.id, t.tag) for t in Tag.query.filter(Tag.user_id == current_user.id)]
    notes = Note.query.order_by(Note.timestamp.desc()).filter(extract('year', Note.timestamp) == year).filter(extract('month', Note.timestamp) == month).filter(Note.user_id == current_user.id)
    return render_template('notes/notes.html', noteForm=noteForm, tagForm=TagForm(), deleteNote=DeleteNote(), notes=notes)

@notes_route.route('/notes/year/<int:year>')
@login_required
def notes_by_year(year):
    noteForm = NoteForm()
    noteForm.tag.choices = [(t.id, t.tag) for t in Tag.query.filter(Tag.user_id == current_user.id)]
    notes = Note.query.order_by(Note.timestamp.desc()).filter(extract('year', Note.timestamp) == year).filter(Note.user_id == current_user.id)
    return render_template('notes/notes.html', noteForm=noteForm, tagForm=TagForm(), deleteNote=DeleteNote(), notes=notes)

@notes_route.route('/notes/day/<int:day>/<int:month>/<int:year>')
@login_required
def notes_by_day(day, month, year):
    noteForm = NoteForm()
    noteForm.tag.choices = [(t.id, t.tag) for t in Tag.query.filter(Tag.user_id == current_user.id)]
    notes = Note.query.order_by(Note.timestamp.desc()).filter(extract('year', Note.timestamp) == year).filter(extract('month', Note.timestamp) == month).filter(extract('day', Note.timestamp) == day).filter(Note.user_id == current_user.id)
    return render_template('notes/notes.html', noteForm=noteForm, tagForm=TagForm(), deleteNote=DeleteNote(), notes=notes)


@notes_route.route('/add-note/', methods=['POST'])
def add_note():
    body = request.form['body']
    public = False
    if body:
        if 'public' in request.form:
            public = True
        tag = Tag.query.filter(Tag.id == request.form['tag']).first()
        note = Note(body=body, user=current_user._get_current_object(), tag=tag, public=public)
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
def note(id):
    note = Note.query.get_or_404(id)
    if not hasattr(current_user, 'id') and note.public == False:
        return abort(403)
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
    return render_template('notes/edit-note.html', noteForm=noteForm, note=note)

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
