import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

from application.build_database import db_load_example_data


def create_app(configs_string):
    app.config.from_object(configs_string)

    db.init_app(app)
    # setup_app_logging(app)
    # setup_routes_logging()

    register_blueprints()
    # deleting pre-existing database for the tests in case test configuration is passed as a parameter
    with app.app_context():
        if os.path.exists("../tests/test.db"):
            os.remove("../tests/test.db")
        db.create_all()
    db_load_example_data(app, db)

    return app


def register_blueprints():
    from .routes.routes_centers import centers
    from .routes.routes_species import species
    from .routes.routes_animals import animals
    app.register_blueprint(centers)
    app.register_blueprint(species)
    app.register_blueprint(animals)


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
