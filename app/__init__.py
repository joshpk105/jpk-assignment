from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = 'Please log in to access this page.'

def create_app(config_class=Config):
    flapp = Flask(__name__)
    flapp.config.from_object(Config)

    # Initilize extensions
    db.init_app(flapp)
    migrate.init_app(flapp)
    login.init_app(flapp)

    # Blueprints
    from app.auth import bp as auth_bp
    flapp.register_blueprint(auth_bp, url_prefix="/auth")

    from app.main import bp as main_bp
    flapp.register_blueprint(main_bp)

    return flapp

from app import models