from flask import render_template
from . import main_route

def render_error(error, code):
    return render_template('errors/error.html', error=error), code

@main_route.app_errorhandler(404)
def page_not_found(e):
    return render_error('page not found', 404)

@main_route.app_errorhandler(403)
def page_forbidden(e):
    return render_error('forbidden', 403)

@main_route.app_errorhandler(500)
def internal_server_error(e):
    return render_error('internal server error', 500)
