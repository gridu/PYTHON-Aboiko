from flask import Blueprint, jsonify, request

from application.animal import get_all_animals, get_animal
from application.center import get_all_centers, get_center
from application.specie import get_all_species, get_specie
from application import app

centers = Blueprint('centers', __name__)

species = Blueprint('species', __name__)

animals = Blueprint('animals', __name__)


@centers.route('/centers')
def get_centers():
    return jsonify({'centers': get_all_centers()})


@centers.route('/centers', methods=['POST'])
def add_center():
    request_data = request.get_json()


@centers.route('/centers/<int:center_id>')
def get_one_center(center_id):
    return jsonify({'center': get_center(center_id)})


@species.route('/species')
def get_species():
    return jsonify({'species': get_all_species()})


@species.route('/species/<int:specie_id>')
def get_one_specie(specie_id):
    return jsonify({'specie': get_specie(specie_id)})


@animals.route('/animals')
def get_animals():
    return jsonify({'animals': get_all_animals()})


@animals.route('/animals/<int:animal_id>')
def get_one_animal(animal_id):
    return jsonify({'animal': get_animal(animal_id)})
