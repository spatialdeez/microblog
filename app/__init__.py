from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_migrate import Migrate # type: ignore
from flask_login import LoginManager # type: ignore
import logging
from logging.handlers import RotatingFileHandler
from flask_mail import Mail # type: ignore
from flask_moment import Moment # type: ignore
from flask_babel import Babel # type: ignore
import os

def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) # database
migrate = Migrate(app, db) # Migration engine
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
moment = Moment(app)
babel = Babel(app, locale_selector=get_locale)

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('[STARTUP] microblog is running!')
from app import routes, models, errors  # This ensures routes are registered

app.shell_context_processor(models.add_shell_context)