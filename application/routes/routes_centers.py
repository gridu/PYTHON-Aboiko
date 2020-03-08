import json

from flask import Blueprint, jsonify, request, Response

from application.custom_logger import log_post_requests
from application.exceptions.validation_exceptions import IncorrectCredentialsException, CenterDoesNotException, \
    CenterAlreadyExistsException
from application.logic.center_logic import get_token, insert_request_access_to_db, get_all_centers, add_center, \
    get_center
from application.util import token_required
from application.validations.center_validations import does_exist, validate_credentials

centers = Blueprint('centers', __name__)


@centers.route('/login')
def login():
    request_data = request.get_json()
    _login = request_data['login']
    _password = request_data['password']
    try:
        does_exist(_login)
    except CenterDoesNotException:
        return jsonify({'message': 'Center {} doesn\'t exist'.format(_login)}), 404
    try:
        validate_credentials(_login, _password)
    except IncorrectCredentialsException:
        return jsonify({'message': 'Wrong credentials'}), 409
    token = get_token(_login)
    insert_request_access_to_db(_login)
    response = Response(
        response='Logged in as {}'.format(_login),
        status=201,
        mimetype='application/json'
    )
    response.headers['x-access-token'] = token
    return response


@centers.route('/centers')
def get_centers():
    return Response(
        response=json.dumps(get_all_centers()),
        status=200,
        mimetype="application/json"
    )


@centers.route('/register', methods=['POST'])
def register():
    request_data = request.get_json()
    _login = request_data['login']
    try:
        new_center = add_center(_login, request_data['password'], request_data['address'])
        center_id = new_center['id']
    except CenterAlreadyExistsException:
        msg = 'Center with {} login already exists'.format(_login)
        return jsonify({"error": msg}), 409
    response = Response(
        response=json.dumps(new_center),
        status=201,
        mimetype="application/json"
    )
    response.headers['Location'] = "/centers/{0}".format(str(center_id))
    log_post_requests(request.method, request.url, center_id, request.path, center_id)
    return response


@token_required
@centers.route('/centers/<int:center_id>')
def get_one_center(_center_id, center_id):
    try:
        return jsonify({'center': get_center(center_id)})
    except CenterDoesNotException:
        msg = 'center you\'re looking for doesn\'t exist'
        return jsonify({"error": msg}), 404