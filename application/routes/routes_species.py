import json

from flask import Blueprint, jsonify, request, Response

from application.custom_logger import log_post_requests
from application.exceptions.validation_exceptions import SpecieDoesNotExistException, SpecieExistsException
from application.logic.specie_logic import get_all_species, get_specie, add_specie
from application.util import token_required

species = Blueprint('species', __name__)

@species.route('/species', methods=['POST', 'GET'])
@token_required
def get_species(_center_id):
    if request.method == 'POST':
        request_data = request.get_json()
        try:
            new_specie = add_specie(request_data['name'],
                                    request_data['price'],
                                    request_data['description'])
        except SpecieExistsException:
            msg = 'That specie already exists'
            return jsonify({"error": msg}), 409
        specie_id = new_specie['specie_id']
        log_post_requests(request.method, request.url, _center_id, request.path, specie_id)
        response = Response("Success", status=201, mimetype='application/json')
        response.headers['Location'] = "/species/" + "id"
        response = Response(
            response=json.dumps(new_specie),
            status=201,
            mimetype='application/json'
        )
        response.headers['Location'] = "/species/{0}".format(str(specie_id))
        return response
    return jsonify({'species': get_all_species()}), 200


@species.route('/species/<int:specie_id>')
def get_one_specie(specie_id):
    try:
        specie = get_specie(specie_id)
        return jsonify({'species': specie})
    except SpecieDoesNotExistException:
        msg = 'Specie you\'re looking for doesn\'t exist'
        return jsonify({"error": msg}), 404