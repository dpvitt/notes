from flask_wtf import Form
from wtforms import SubmitField, TextAreaField, SelectField, StringField
from wtforms.validators import Required, Length, Regexp

class NoteForm(Form):
    body = TextAreaField('What is on your mind?', validators=[Required()])
    tag = SelectField('Tag')
    submitNote = SubmitField('submit')

class EditForm(Form):
    body = TextAreaField('What is on your mind?', validators=[Required()])
    submitNote = SubmitField('submit')

class DeleteNote(Form):
    submit = SubmitField('Delete')

class TagForm(Form):
    tag = StringField('Tag')
    submitTag = SubmitField('submit')
