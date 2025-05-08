from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_migrate import Migrate # type: ignore
from flask_login import LoginManager # type: ignore

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) # database
migrate = Migrate(app, db) # Migration engine
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors  # This ensures routes are registered

app.shell_context_processor(models.add_shell_context)