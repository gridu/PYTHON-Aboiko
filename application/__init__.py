import os

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