from flask_wtf import Form
from wtforms import SubmitField, TextAreaField
from wtforms.validators import Required

class NoteForm(Form):
    body = TextAreaField('What is on your mind?', validators=[Required()])
    submit = SubmitField('Submit')

class DeleteNote(Form):
    submit = SubmitField('Delete')
