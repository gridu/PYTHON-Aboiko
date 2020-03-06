import datetime
import json
from functools import wraps
import jwt
from flask import jsonify, request

from settings import Config
from . import db
from .access_request import Access_Request
from .exceptions.validation_exceptions import CenterAlreadyExistsException, CenterDoesNotException


def make_json(self):
    return {
        'id': self.id,
        'login': self.login,
        'pass': self.password,
        'address': self.address
    }


# def make_json_creds(self):
#     return {
#         'login': self.login,
#         'password': self.password
#     }


def get_all_centers():
    return [make_json(center) for center in Center.query.all()]


from .util import generate_hash, verify_hash


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
    print(make_json(new_center))
    db.session.add(new_center)
    db.session.commit()
    return make_json(new_center)


class Center(db.Model):
    __tablename__ = "center"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    address = db.Column(db.String(32))

    animals = db.relationship(
        "Animal",
        backref="center",
        cascade="all, delete, save-update, delete-orphan",
        single_parent=True,
    )

    def __repr__(self):
        center_object = {
            'login': self.login,
            'address': self.address,
            # 'animals': self.animals
        }
        return json.dumps(center_object)


def get_token(_login):
    # _center_id = find_by_login(_login).id
    # expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    token_payload = generate_token_payload(_login)
    token = jwt.encode({'id': token_payload[0],
                        'exp': token_payload[1]},
                       Config.JWT_SECRET_KEY)

    # print(token)
    # return jsonify({'token': token.decode('UTF-8')})
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
