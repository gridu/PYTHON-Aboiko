import datetime

import jwt

from application import db
from application.access_request import Access_Request
from application.models.center import make_json, Center
from application.exceptions.validation_exceptions import CenterDoesNotException, CenterAlreadyExistsException
from application.util import generate_hash
from settings import Config


def get_all_centers():
    return [make_json(center) for center in Center.query.all()]


def find_by_login(_login):
    return Center.query.filter_by(login=_login).one_or_none()


def get_center(_center_id):
    center = Center.query.get(_center_id)
    if center is None:
        raise CenterDoesNotException
    return make_json(center)


def add_center(_login, _password, _address):
    existing_center = find_by_login(_login)
    if existing_center is not None:
        raise CenterAlreadyExistsException
    new_center = Center(login=_login, password=generate_hash(_password), address=_address)
    db.session.add(new_center)
    db.session.commit()
    return make_json(new_center)

def get_token(_login):

    token_payload = generate_token_payload(_login)
    token = jwt.encode({'id': token_payload[0],
                        'exp': token_payload[1]},
                       Config.JWT_SECRET_KEY)

    return token


def insert_request_access_to_db(_login):
    token_payload = generate_token_payload(_login)
    access_request = Access_Request(center_id=token_payload[0],
                                    timestamp=token_payload[1])
    db.session.add(access_request)
    db.session.commit()


def generate_token_payload(_login):
    _center_id = find_by_login(_login).id
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    return _center_id, expiration_time