from functools import wraps

import jwt
from flask import request, jsonify
from passlib.hash import pbkdf2_sha256 as sha256

from settings import Config


def generate_hash(password):
    return sha256.hash(password)


def verify_hash(password, hash):
    return sha256.verify(password, hash)


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
            # current_center = Center.query.get(request_data['id'])
            _center_id = request_data['id']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(_center_id, *args, **kwargs)

    return decorated
