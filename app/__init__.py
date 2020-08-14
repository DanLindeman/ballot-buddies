import quart.flask_patch

from pathlib import Path
from sqlite3 import dbapi2 as sqlite3

from .config import Config
from flask_sqlalchemy import SQLAlchemy

from quart import Quart, redirect, request, render_template, url_for, session
from .config import Config

app = Quart(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
db.init_app(app)

app.config.update({
    'DATABASE': app.root_path / 'app.db',
})

from app import routes, models