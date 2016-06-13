from flask import Blueprint

main_route = Blueprint('main_route', __name__)

from . import views, errors
