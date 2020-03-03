# Local modules
from flask import Flask

from settings import app


def create_app():
    #from . import models
    from app import routes
    app1 = Flask(__name__)
    #models.init_app(app)
    #routes.init_app(app)
    return app1


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

# app.run(port=5000)
