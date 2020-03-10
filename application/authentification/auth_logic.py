import datetime
from functools import wraps

import jwt
from flask import request, jsonify, make_response

from application import db
from application.validations.center_validations import find_by_login
from application.authentification.accessrequest import AccessRequest
from settings import Config


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            request_data = jwt.decode(token, Config.JWT_SECRET_KEY)
            _center_id = request_data['id']
            # could be used for the test !!!
            # access_req=AccessRequest.query.filter_by(center_id=_center_id).first()
            # if access_req.timestamp < datetime.datetime.utcnow()
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({'message': 'Signature expired. Please log in again'}), 401)
        except jwt.InvalidTokenError:
            return make_response(jsonify({'message': 'Token is invalid!'}), 401)

        return f(_center_id, *args, **kwargs)

    return decorated


def get_token(_login):
    token_payload = generate_token_payload(_login)
    token = jwt.encode({'id': token_payload[0],
                        'exp': token_payload[1]},
                       Config.JWT_SECRET_KEY)

    return token


def insert_request_access_to_db(_login):
    token_payload = generate_token_payload(_login)
    access_request = AccessRequest(center_id=token_payload[0],
                                   timestamp=token_payload[1])
    db.session.add(access_request)
    db.session.commit()


def generate_token_payload(_login):
    _center_id = find_by_login(_login).id
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    return _center_id, expiration_time
