from flask import Blueprint, jsonify

from application.animal import get_all_animals
from application.center import get_all_centers
from application.specie import get_all_species
from application import app

centers = Blueprint('centers', __name__)

species = Blueprint('species', __name__)

animals = Blueprint('animals', __name__)


# GET ALL routes

@centers.route('/centers')
def get_centers():
    return jsonify({'centers': get_all_centers()})


@species.route('/species')
def get_species():
    return jsonify({'species': get_all_species()})


@animals.route('/animals')
def get_animals():
    return jsonify({'animals': get_all_animals()})
