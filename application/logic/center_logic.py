import json

from flask import make_response, jsonify, Response

from application import db
from application.models.center import make_json, Center
from application.util import generate_hash
from application.validations.center_validations import does_exist, validate_credentials, find_by_login
from application.authentification.auth_logic import get_token, insert_request_access_to_db


def login_center(_login, _password):
    """
    This function registers a new center

    :param _login        Login of the center to login with
    :param _password     Password of the center to login with
    :return:             success (200), 404 if center doesn't exist,
                         409 for wrong credentials
    """
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
    """
    This function returns all registered centers as a response for the route /centers
    """
    return make_response(jsonify([make_json(center) for center in Center.query.all()]), 200)


def get_center(center_id):
    """
    This function registers a new center

    :param center_id     Login of the center to obtain
    :return:            JSON of center data on success (200),
                        404 if center doesn't exist
    """
    center = Center.query.get(center_id)
    if center is None:
        msg = 'center you\'re looking for doesn\'t exist'
        return make_response(jsonify({"error": msg}), 404)
    return make_response(make_json(center), 200)


def add_center(_login, _password, _address):
    """
    This function registers a new center

    :param _login       Login of the center to register
    :param _password    Password of the center to register
    :param _address     Address of the center to register
    :return:            200 on successful register, 409 if center exists
    """

    if does_exist(_login):
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

