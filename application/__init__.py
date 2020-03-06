import os
from time import asctime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from application.animal import Animal
# from application.center import Center
# from application.specie import Specie

db = SQLAlchemy()
app = Flask(__name__)

from application.build_database import db_load_example_data


def create_app():
    app.config.from_object('settings.Config')

    db.init_app(app)
    setup_logging(app)

    from .routes import centers
    from .routes import species
    from .routes import animals
    app.register_blueprint(centers)
    app.register_blueprint(species)
    app.register_blueprint(animals)
    with app.app_context():
        if os.path.exists("sale_animal.db"):
            os.remove("sale_animal.db")
        db.create_all()
    db_load_example_data(app, db)

    return app


def setup_logging(app):
    import logging
    from logging import FileHandler
    log_handler_file = FileHandler('requests.log')
    log_handler_file.setLevel(logging.INFO)
    app.logger.addHandler(log_handler_file)
