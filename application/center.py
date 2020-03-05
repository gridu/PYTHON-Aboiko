import datetime
import json
from functools import wraps
import jwt
from flask import jsonify, request

from settings import Config
from . import db


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


def validate_credentials(_login, _password):
    center = find_by_login(_login)
    if center is None:
        return False
    # valid_pas = (center.password == _password)
    valid_pas = verify_hash(_password, center.password)
    return valid_pas


def does_exist(_login):
    center = find_by_login(_login)
    if center is None:
        return False
    return True


def find_by_login(_login):
    return Center.query.filter_by(login=_login).one_or_none()


def get_center(_center_id):
    # return make_json(Center.query.filter_by(id=_center_id).first())
    return make_json(Center.query.get(_center_id))


def add_center(_login, _password, _address):
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
    center = find_by_login(_login)
    token = jwt.encode({'id': center.id,
                        'exp': datetime.datetime.utcnow()
                               + datetime.timedelta(minutes=30)},
                       Config.JWT_SECRET_KEY)
    # print(token)
    # return jsonify({'token': token.decode('UTF-8')})
    return token



