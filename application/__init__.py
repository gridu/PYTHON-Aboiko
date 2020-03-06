import os
from time import asctime
import logging
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
    setup_app_logging(app)
    # setup_routes_logging()

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


def setup_app_logging(app):
    # log_handler_file = FileHandler('appevents.log')
    # log_handler_file.setLevel(logging.INFO)
    # app.logger.addHandler(log_handler_file)
    # if not app.debug:
    # logging.basicConfig(filename='appevents.log', level=logging.WARNING,
    #                     format='%(levelname)s:%(message)s')
    pass
# def setup_routes_logging():
#     logger = logging.getLogger(__name__)
#     app_logger = logging.FileHandler('requests.log')
#     logger.setLevel(logging.INFO)
#     format_custom_logger = logging.Formatter("%(asctime)s %(message)s")
#     app_logger.setFormatter(format_custom_logger)
#     logger.addHandler(app_logger)
