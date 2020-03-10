from flask import Blueprint, jsonify, request
from flask_expects_json import expects_json
from application.custom_logger import log_put_delete_requests, log_post_requests
from application.logic.animal_logic import add_animal, get_all_animals_for_center, update_animal, \
    delete_animal, get_animal
from application.schemas import post_animal_schema, put_animal_schema
from application.authentification.auth_logic import token_required

animals = Blueprint('animals', __name__)


@animals.route('/animals', methods=['GET'])
@token_required
def get_animals(_center_id):
    # get all the animals related to the center

    return jsonify({'animals': get_all_animals_for_center(_center_id)})


@animals.route('/animals', methods=['POST'])
@token_required
@expects_json(post_animal_schema)
def post_animal(_center_id):
    # post an animal to the current center animals list

    request_data = request.get_json()
    response = add_animal(_center_id, request_data['name'],
                          request_data['age'],
                          request_data['specie'])
    if response.status_code == 201:
        log_post_requests(request.method, request.url, _center_id,
                          request.path, response.json['id'])
    return response


@animals.route('/animals/<int:animal_id>', methods=['GET', 'DELETE'])
@token_required
def get_or_delete_animal(_center_id, animal_id):
    # either get or delete provided animal id

    if request.method == 'DELETE':
        response = delete_animal(_center_id, animal_id)
        if response.status_code == 200:
            log_put_delete_requests(request.method, request.url, _center_id, request.path)
        return response

    return get_animal(_center_id, animal_id)


@animals.route('/animals/<int:animal_id>', methods=['PUT'])
@token_required
@expects_json(put_animal_schema)
def put_animal(_center_id, animal_id):
    # changing animal data

    request_data = request.get_json()
    new_animal_data = (animal_id, _center_id, request_data['name'], request_data['age'], request_data['specie'])
    response = update_animal(new_animal_data)
    if response.status_code == 200:
        log_put_delete_requests(request.method, request.url, _center_id, request.path)
    return response
