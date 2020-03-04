# Local modules
from flask import Flask

# from settings import application
#
#
# def create_app():
#     #from . import models
#     from application import routes
#     app1 = Flask(__name__)
#     #models.init_app(application)
#     routes.init_app(app1)
#     return app1
from application import create_app

app = create_app()

#
# @application.route('/test')
# def get_species():
#     return "jsonify it"

if __name__ == "__main__":
    app.run(debug=True)

# application.run(port=5000)
