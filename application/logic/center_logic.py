import json

from flask import make_response, jsonify, Response

from application import db
from application.models.center import make_json, Center
from application.util import generate_hash
from application.validations.center_validations import does_exist, validate_credentials, find_by_login
from authentification.auth_logic import get_token, insert_request_access_to_db


def login_center(_login, _password):
    if not does_exist(_login):
        return make_response(jsonify({'message': 'Center {} doesn\'t exist'.format(_login)}), 404)

    if not validate_credentials(_login, _password):
        return make_response(jsonify({'message': 'Wrong credentials'}), 409)

    token = get_token(_login)
    insert_request_access_to_db(_login)

    response = Response(
        response='Logged in as {}'.format(_login),
        status=200,
        mimetype='application/json'
    )
    response.headers['x-access-token'] = token
    return response


def get_all_centers():
    return make_response(jsonify([make_json(center) for center in Center.query.all()]), 200)


def get_center(center_id):
    center = Center.query.get(center_id)
    if center is None:
        msg = 'center you\'re looking for doesn\'t exist'
        return make_response(jsonify({"error": msg}), 404)
    return make_response(make_json(center), 200)


def add_center(_login, _password, _address):
    existing_center = find_by_login(_login)
    if existing_center is not None:
        msg = 'Center with {} login already exists'.format(_login)
        return make_response(jsonify({"error": msg}), 409)
    new_center = Center(login=_login, password=generate_hash(_password), address=_address)
    db.session.add(new_center)
    db.session.commit()
    response = Response(
        response=json.dumps(make_json(new_center)),
        status=201,
        mimetype="application/json"
    )
    response.headers['Location'] = "/centers/{0}".format(str(new_center.id))
    return response

