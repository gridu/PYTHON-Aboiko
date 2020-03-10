import datetime
from functools import wraps

import jwt
from flask import request, jsonify, make_response

from application import db
from application.validations.center_validations import find_by_login
from application.authentification.accessrequest import AccessRequest
from settings import Config


def token_required(f):
    # a decorator to wrap function f in a function which checks token correctness

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            request_data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
            _center_id = request_data['id']
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({'message': 'Signature expired. Please log in again'}), 401)
        except jwt.InvalidTokenError:
            return make_response(jsonify({'message': 'Token is invalid!'}), 401)

        return f(_center_id, *args, **kwargs)

    return decorated


def get_token(_login):
    # function which encodes token with provided secret key and algorithm

    token_payload = generate_token_payload(_login)
    token = jwt.encode({'id': token_payload[0],
                        'exp': token_payload[1]},
                       Config.JWT_SECRET_KEY, Config.JWT_ALGORITHM)

    return token


def insert_request_access_to_db(_login):
    # inserting access request to database

    token_payload = generate_token_payload(_login)
    access_request = AccessRequest(center_id=token_payload[0],
                                   timestamp=token_payload[1])
    db.session.add(access_request)
    db.session.commit()


def generate_token_payload(_login):
    # function which generates token payload

    _center_id = find_by_login(_login).id
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    return _center_id, expiration_time
