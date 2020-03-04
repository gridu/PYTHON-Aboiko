from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    #from . import models
    from application import routes
    app = Flask(__name__)
    app.config.from_object('settings.Config')

    #models.init_app(application)
    routes.init_app(app)

    db.init_app(app)
    with app.app_context():
        from application import routes
        from models import animal, center, specie
        return app
