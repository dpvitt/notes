from flask import Blueprint

notes_route = Blueprint('notes_route', __name__)

from . import views
