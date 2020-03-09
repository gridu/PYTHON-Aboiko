from flask import Blueprint, request
from flask_expects_json import expects_json

from application.custom_logger import log_post_requests
from application.logic.specie_logic import get_all_species, get_specie, add_specie
from application.schemas import post_specie_schema
from authentification.auth_logic import token_required

species = Blueprint('species', __name__)


@species.route('/species', methods=['GET'])
@token_required
def get_species(_center_id):
    return get_all_species()


@species.route('/species', methods=['POST'])
@token_required
@expects_json(post_specie_schema)
def post_specie(_center_id):
    request_data = request.get_json()
    response = add_specie(request_data['name'],
                          request_data['price'],
                          request_data['description'])
    if response.status_code == 201:
        log_post_requests(request.method, request.url, _center_id, request.path,
                          response.json['specie_id'])
    return response


@species.route('/species/<int:specie_id>')
def get_one_specie(specie_id):
    return get_specie(specie_id)
