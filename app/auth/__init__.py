from flask import Blueprint

auth_route = Blueprint('auth_route', __name__)

from . import views
