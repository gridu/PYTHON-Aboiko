from flask import Blueprint, jsonify, request, Response, make_response

from application.animal import get_all_animals, get_animal, add_animal, update_animal, Animal, delete_animal
from application.center import *
from application.specie import get_all_species, get_specie, add_specie

centers = Blueprint('centers', __name__)

species = Blueprint('species', __name__)

animals = Blueprint('animals', __name__)


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
            current_center = find_by_login(request_data['login'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_center, *args, **kwargs)

    return decorated


@centers.route('/login')
def login():
    request_data = request.get_json()
    _login = request_data['login']
    _password = request_data['password']
    exists = does_exist(_login)
    if exists:
        creds_valid = validate_credentials(_login, _password)
        if creds_valid:
            print(get_token(_login))
            return {'message': 'Logged in as {}'.format(_login)}
        else:
            return {'message': 'Wrong credentials'}
    else:
        return {'message': 'Center {} doesn\'t exist'.format(_login)}


@centers.route('/centers')
def get_centers(current_center):
    return jsonify({'centers': get_all_centers()})


@centers.route('/register', methods=['POST'])
def register():
    request_data = request.get_json()
    add_center(request_data['login'], request_data['password'], request_data['address'])
    response = Response("", status=201, mimetype='application/json')
    response.headers['Location'] = "/centers/" + "id"
    return response


@centers.route('/centers/<int:center_id>')
def get_one_center(center_id):
    return jsonify({'center': get_center(center_id)})


@token_required
@species.route('/species', methods=['POST', 'GET'])
def get_species():
    if request.method == 'POST':
        request_data = request.get_json()
        add_specie(request_data['name'], request_data['price'], request_data['description'])
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/species/" + "id"
        return response
    return jsonify({'species': get_all_species()})


@species.route('/species/<int:specie_id>')
def get_one_specie(specie_id):
    return jsonify({'specie': get_specie(specie_id)})


@token_required
@animals.route('/animals', methods=['GET', 'POST'])
def get_animals():
    if request.method == 'POST':
        request_data = request.get_json()
        add_animal(request_data['center_id'], request_data['name'], request_data['age'], request_data['specie'])
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/animals/" + "id"
        return response
    return jsonify({'animals': get_all_animals()})


@token_required
@animals.route('/animals/<int:animal_id>', methods=['GET', 'DELETE', 'PUT'])
def get_one_animal(animal_id):
    if request.method == 'PUT':
        request_data = request.get_json()
        new_animal = Animal()
        new_animal.center_id = request_data['center_id']
        new_animal.name = request_data['name']
        new_animal.age = request_data['age']
        new_animal.specie = request_data['specie']
        update_animal(animal_id, new_animal)
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/animals/" + str(animal_id)
        return response
    elif request.method == 'DELETE':
        delete_animal(animal_id)
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/animals/" + str(animal_id)
        return response
    return jsonify({'animal': get_animal(animal_id)})
