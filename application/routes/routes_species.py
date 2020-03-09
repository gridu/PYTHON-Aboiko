from flask import Blueprint, request

from application.custom_logger import log_post_requests
from application.logic.specie_logic import get_all_species, get_specie, add_specie
from application.util import token_required

species = Blueprint('species', __name__)


@species.route('/species', methods=['POST', 'GET'])
@token_required
def get_species(_center_id):
    if request.method == 'POST':
        request_data = request.get_json()
        response = add_specie(request_data['name'],
                              request_data['price'],
                              request_data['description'])
        if response.status_code == 201:
            log_post_requests(request.method, request.url, _center_id, request.path,
                              response.json['specie_id'])
        return response

    return get_all_species()


@species.route('/species/<int:specie_id>')
def get_one_specie(specie_id):
    return get_specie(specie_id)
