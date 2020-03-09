from flask import Blueprint, jsonify, request

from application.custom_logger import log_put_delete_requests, log_post_requests
from application.logic.animal_logic import add_animal, get_all_animals_for_center, update_animal, \
    delete_animal, get_animal
from application.util import token_required

animals = Blueprint('animals', __name__)


@animals.route('/animals', methods=['GET', 'POST'])
@token_required
def get_animals(_center_id):
    if request.method == 'POST':
        request_data = request.get_json()
        response = add_animal(_center_id, request_data['name'],
                              request_data['age'],
                              request_data['specie'])
        if response.status_code == 201:
            log_post_requests(request.method, request.url, _center_id,
                              request.path, response.json['id'])
        return response

    return jsonify({'animals': get_all_animals_for_center(_center_id)})


@animals.route('/animals/<int:animal_id>', methods=['GET', 'DELETE', 'PUT'])
@token_required
def get_one_animal(_center_id, animal_id):
    if request.method == 'PUT':
        request_data = request.get_json()
        new_animal_data = (animal_id, _center_id, request_data['name'], request_data['age'], request_data['specie'])
        response = update_animal(animal_id, new_animal_data)
        if response.status_code == 200:
            log_put_delete_requests(request.method, request.url, _center_id, request.path)
        return response

    elif request.method == 'DELETE':
        response = delete_animal(_center_id, animal_id)
        if response.status_code == 200:
            log_put_delete_requests(request.method, request.url, _center_id, request.path)
        return response

    return get_animal(_center_id, animal_id)
