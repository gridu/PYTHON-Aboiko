from flask import Blueprint, request

from application.custom_logger import log_post_requests
from application.logic.center_logic import get_all_centers, add_center, \
    get_center, login_center

centers = Blueprint('centers', __name__)


@centers.route('/login')
def login():
    request_data = request.get_json()
    _login = request_data['login']
    _password = request_data['password']
    return login_center(_login, _password)


@centers.route('/centers')
def get_centers():
    return get_all_centers()


@centers.route('/register', methods=['POST'])
def register():
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
    return get_center(center_id)
