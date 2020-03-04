from flask_sqlalchemy import SQLAlchemy

from run import app
from settings import Config

app.config.from_object(Config)
db = SQLAlchemy(app)