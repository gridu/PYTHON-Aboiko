import json

from flask import Blueprint, jsonify, request, Response

from application.custom_logger import log_put_delete_requests, log_post_requests
from application.exceptions.validation_exceptions import AnimalExistsException, AnimalNotFoundException, \
    IncorrectCredentialsException, SpecieDoesNotExistException
from application.logic.animal_logic import add_animal, get_all_animals_for_center, is_center_id_valid, update_animal, \
    delete_animal, get_animal
from application.util import token_required

animals = Blueprint('animals', __name__)


@animals.route('/animals', methods=['GET', 'POST'])
@token_required
def get_animals(_center_id):
    if request.method == 'POST':
        request_data = request.get_json()
        try:
            new_animal = add_animal(_center_id, request_data['name'],
                                    request_data['age'],
                                    request_data['specie'])
            animal_id = new_animal['id']
        except AnimalExistsException:
            msg = 'That animal already exists'
            return jsonify({"error": msg}), 409
        except SpecieDoesNotExistException:
            msg = 'You\'re trying to assign an animal to not existing specie'
            return jsonify({"error": msg}), 409
        response = Response(
            response=json.dumps(new_animal),
            status=201,
            mimetype='application/json'
        )
        response.headers['Location'] = "/animals/{0}".format(str(animal_id))
        log_post_requests(request.method, request.url, _center_id, request.path, animal_id)
        return response

    return jsonify({'animals': get_all_animals_for_center(_center_id)})


@animals.route('/animals/<int:animal_id>', methods=['GET', 'DELETE', 'PUT'])
@token_required
def get_one_animal(_center_id, animal_id):
    if request.method == 'PUT':
        request_data = request.get_json()
        try:
            is_center_id_valid(_center_id, animal_id)
        except IncorrectCredentialsException:
            msg = 'you\'re trying to update an animal which isn\'t related to your id'
            return jsonify({"error": msg}), 409
        new_animal_data = (animal_id, _center_id, request_data['name'], request_data['age'], request_data['specie'])
        try:
            update_animal(new_animal_data)
        except:
            msg = 'You\'re trying to update an animal of not existing specie'
            return jsonify({"error": msg}), 409
        log_put_delete_requests(request.method, request.url, _center_id, request.path)
        msg = "an animal updated successfully"
        return jsonify({"success": msg}), 200

    elif request.method == 'DELETE':
        try:
            is_center_id_valid(_center_id, animal_id)
        except IncorrectCredentialsException:
            msg = 'you\'re trying to delete an animal which isn\'t related to your id'
            return jsonify({"error": msg}), 409
        except AnimalNotFoundException:
            msg = 'you\'re trying to delete an animal which doesn\'t exist'
            return jsonify({"error": msg}), 404
        log_put_delete_requests(request.method, request.url, _center_id, request.path)

        delete_animal(animal_id)

        msg = "an animal deleted successfully"
        return jsonify({"success": msg}), 204

    try:
        is_center_id_valid(_center_id, animal_id)
    except IncorrectCredentialsException:
        msg = 'you\'re trying to view the animal which isn\'t related to your id'
        return jsonify({"error": msg}), 409
    except AnimalNotFoundException:
        msg = 'you\'re looking for an animal which doesn\'t exist'
        return jsonify({"error": msg}), 404
    return jsonify(get_animal(animal_id)), 200