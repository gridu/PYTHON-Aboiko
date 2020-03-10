from flask import Blueprint, request
from flask_expects_json import expects_json
from application.custom_logger import log_post_requests
from application.logic.center_logic import get_all_centers, add_center, \
    get_center, login_center
from application.schemas import register_schema, login_schema

centers = Blueprint('centers', __name__)


@centers.route('/login')
@expects_json(login_schema)
def login():
    # login with provided credentials

    request_data = request.get_json()
    _login = request_data['login']
    _password = request_data['password']
    return login_center(_login, _password)


@centers.route('/centers')
def get_centers():
    # get all registered centers

    return get_all_centers()


@centers.route('/register', methods=['POST'])
@expects_json(register_schema)
def register():
    # register new center

    request_data = request.get_json()
    response = add_center(request_data['login'],
                          request_data['password'],
                          request_data['address'])
    if response.status_code == 201:
        log_post_requests(request.method, request.url,
                          response.json['id'], request.path,
                          response.json['id'])
    return response


@centers.route('/centers/<int:center_id>')
def get_one_center(center_id):
    # get a center data with provided id

    return get_center(center_id)
