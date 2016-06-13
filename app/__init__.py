from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth_route.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main_route as main_blueprint
    app.register_blueprint(main_blueprint)

    from .notes import notes_route as notes_blueprint
    app.register_blueprint(notes_blueprint)

    from .auth import auth_route as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
