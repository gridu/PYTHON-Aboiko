from flask import Blueprint, jsonify, request, Response, make_response
from jsonschema import ValidationError

from application.animal import get_all_animals, get_animal, add_animal, update_animal, Animal, delete_animal, \
    get_all_animals_for_center, is_center_id_valid
from application.center import *
from application.exceptions.validation_exceptions import AnimalExistsException, AnimalNotFoundException, \
    IncorrectCredentialsException, CenterDoesNotException, SpecieDoesNotExistException
from application.specie import get_all_species, get_specie, add_specie

from application.validations.center_validations import does_exist, validate_credentials

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
            # current_center = Center.query.get(request_data['id'])
            _center_id = request_data['id']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(_center_id, *args, **kwargs)

        # return f(*args, **kwargs)

    return decorated


@centers.route('/login')
def login():
    request_data = request.get_json()
    _login = request_data['login']
    _password = request_data['password']
    try:
        does_exist(_login)
    except CenterDoesNotException:
        return jsonify({'message': 'Center {} doesn\'t exist'.format(_login)}), 404
    try:
        validate_credentials(_login, _password)
    except IncorrectCredentialsException:
        return jsonify({'message': 'Wrong credentials'}), 409
    token = get_token(_login)
    insert_request_access_to_db(_login)
    response = Response('Logged in as {}'.format(_login), status=201, mimetype='application/json')
    response.headers['x-access-token'] = token
    return response


@centers.route('/centers')
def get_centers():
    return jsonify({'centers': get_all_centers()})


@centers.route('/register', methods=['POST'])
def register():
    request_data = request.get_json()
    try:
        add_center(request_data['login'], request_data['password'], request_data['address'])
    except CenterAlreadyExistsException:
        msg = 'Center with {} login already exists'.format(request_data['login'])
        return jsonify({"error": msg}), 409
    response = Response("", status=201, mimetype='application/json')
    response.headers['Location'] = "/centers/" + "id"
    return response


@token_required
@centers.route('/centers/<int:center_id>')
def get_one_center(_center_id, center_id):
    try:
        return jsonify({'center': get_center(center_id)})
    except CenterDoesNotException:
        msg = 'center you\'re looking for doesn\'t exist'
        return jsonify({"error": msg}), 404


@species.route('/species', methods=['POST', 'GET'])
@token_required
def get_species(_center_id):
    if request.method == 'POST':
        request_data = request.get_json()
        add_specie(request_data['name'], request_data['price'], request_data['description'])
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/species/" + "id"
        return response
    return jsonify({'species': get_all_species()})


@species.route('/species/<int:specie_id>')
def get_one_specie(specie_id):
    try:
        specie = get_specie(specie_id)
        return jsonify({'specie': specie})
    except SpecieDoesNotExistException:
        msg = 'Specie you\'re looking for doesn\'t exist'
        return jsonify({"error": msg}), 404


@animals.route('/animals', methods=['GET', 'POST'])
@token_required
def get_animals(_center_id):
    if request.method == 'POST':
        request_data = request.get_json()
        try:
            add_animal(_center_id, request_data['name'], request_data['age'], request_data['specie'])
        except AnimalExistsException:
            msg = 'That animal already exists'
            return jsonify({"error": msg}), 409
        except SpecieDoesNotExistException:
            msg = 'You\'re trying to assign an animal to not existing specie'
            return jsonify({"error": msg}), 409
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/animals/" + "id"
        return response
    # return jsonify({'animals': get_all_animals()})
    return jsonify({'animals': get_all_animals_for_center(_center_id)})


@animals.route('/animals/<int:animal_id>', methods=['GET', 'DELETE', 'PUT'])
@token_required
def get_one_animal(_center_id, animal_id):
    if request.method == 'PUT':
        request_data = request.get_json()
        try:
            is_center_id_valid(_center_id, animal_id)
        except IncorrectCredentialsException:
            msg = 'you\'re trying to update an animal which isn\'t related to your id'
            return jsonify({"error": msg}), 409
        new_animal = Animal()
        new_animal.center_id = _center_id
        new_animal.name = request_data['name']
        new_animal.age = request_data['age']
        new_animal.specie = request_data['specie']
        update_animal(animal_id, new_animal)
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/animals/" + str(animal_id)
        return response
    elif request.method == 'DELETE':
        try:
            is_center_id_valid(_center_id, animal_id)
        except IncorrectCredentialsException:
            msg = 'you\'re trying to delete an animal which isn\'t related to your id'
            return jsonify({"error": msg}), 409
        delete_animal(animal_id)
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/animals/" + str(animal_id)
        return response
    try:
        return jsonify({'animal': get_animal(animal_id)})
    except AnimalNotFoundException:
        msg = 'you\'re looking for an animal which doesn\'t exist'
        return jsonify({"error": msg}), 409
