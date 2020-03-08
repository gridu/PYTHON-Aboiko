# import json
#
# from flask import Blueprint, jsonify, request, Response
#
#
# from application.custom_logger import log_put_delete_requests, log_post_requests
# from application.exceptions.validation_exceptions import AnimalExistsException, AnimalNotFoundException, \
#     IncorrectCredentialsException, CenterDoesNotException, SpecieDoesNotExistException, CenterAlreadyExistsException, \
#     SpecieExistsException
# from application.logic.animal_logic import add_animal, get_all_animals_for_center, is_center_id_valid, update_animal, \
#     delete_animal, get_animal
# from application.logic.center_logic import get_token, insert_request_access_to_db, get_all_centers, add_center, \
#     get_center
# from application.logic.specie_logic import get_all_species, get_specie, add_specie
# from application.util import token_required
#
# from application.validations.center_validations import does_exist, validate_credentials
#
#
# centers = Blueprint('centers', __name__)
#
# species = Blueprint('species', __name__)
#
# animals = Blueprint('animals', __name__)
#
#
#
#
#
# @centers.route('/login')
# def login():
#     request_data = request.get_json()
#     _login = request_data['login']
#     _password = request_data['password']
#     try:
#         does_exist(_login)
#     except CenterDoesNotException:
#         return jsonify({'message': 'Center {} doesn\'t exist'.format(_login)}), 404
#     try:
#         validate_credentials(_login, _password)
#     except IncorrectCredentialsException:
#         return jsonify({'message': 'Wrong credentials'}), 409
#     token = get_token(_login)
#     insert_request_access_to_db(_login)
#     response = Response(
#         response='Logged in as {}'.format(_login),
#         status=201,
#         mimetype='application/json'
#     )
#     response.headers['x-access-token'] = token
#     return response
#
#
# @centers.route('/centers')
# def get_centers():
#     return Response(
#         response=json.dumps(get_all_centers()),
#         status=200,
#         mimetype="application/json"
#     )
#
#
# @centers.route('/register', methods=['POST'])
# def register():
#     request_data = request.get_json()
#     _login = request_data['login']
#     try:
#         new_center = add_center(_login, request_data['password'], request_data['address'])
#         center_id = new_center['id']
#     except CenterAlreadyExistsException:
#         msg = 'Center with {} login already exists'.format(_login)
#         return jsonify({"error": msg}), 409
#     response = Response(
#         response=json.dumps(new_center),
#         status=201,
#         mimetype="application/json"
#     )
#     response.headers['Location'] = "/centers/{0}".format(str(center_id))
#     log_post_requests(request.method, request.url, center_id, request.path, center_id)
#     return response
#
#
# @token_required
# @centers.route('/centers/<int:center_id>')
# def get_one_center(_center_id, center_id):
#     try:
#         return jsonify({'center': get_center(center_id)})
#     except CenterDoesNotException:
#         msg = 'center you\'re looking for doesn\'t exist'
#         return jsonify({"error": msg}), 404
#
#
# @species.route('/species', methods=['POST', 'GET'])
# @token_required
# def get_species(_center_id):
#     if request.method == 'POST':
#         request_data = request.get_json()
#         try:
#             new_specie = add_specie(request_data['name'],
#                                     request_data['price'],
#                                     request_data['description'])
#         except SpecieExistsException:
#             msg = 'That specie already exists'
#             return jsonify({"error": msg}), 409
#         specie_id = new_specie['specie_id']
#         log_post_requests(request.method, request.url, _center_id, request.path, specie_id)
#         response = Response("Success", status=201, mimetype='application/json')
#         response.headers['Location'] = "/species/" + "id"
#         response = Response(
#             response=json.dumps(new_specie),
#             status=201,
#             mimetype='application/json'
#         )
#         response.headers['Location'] = "/species/{0}".format(str(specie_id))
#         return response
#     return jsonify({'species': get_all_species()}), 200
#
#
# @species.route('/species/<int:specie_id>')
# def get_one_specie(specie_id):
#     try:
#         specie = get_specie(specie_id)
#         return jsonify({'species': specie})
#     except SpecieDoesNotExistException:
#         msg = 'Specie you\'re looking for doesn\'t exist'
#         return jsonify({"error": msg}), 404
#
#
# @animals.route('/animals', methods=['GET', 'POST'])
# @token_required
# def get_animals(_center_id):
#     if request.method == 'POST':
#         request_data = request.get_json()
#         try:
#             new_animal = add_animal(_center_id, request_data['name'],
#                                     request_data['age'],
#                                     request_data['specie'])
#             animal_id = new_animal['id']
#         except AnimalExistsException:
#             msg = 'That animal already exists'
#             return jsonify({"error": msg}), 409
#         except SpecieDoesNotExistException:
#             msg = 'You\'re trying to assign an animal to not existing specie'
#             return jsonify({"error": msg}), 409
#         response = Response(
#             response=json.dumps(new_animal),
#             status=201,
#             mimetype='application/json'
#         )
#         response.headers['Location'] = "/animals/{0}".format(str(animal_id))
#         log_post_requests(request.method, request.url, _center_id, request.path, animal_id)
#         return response
#
#     return jsonify({'animals': get_all_animals_for_center(_center_id)})
#
#
# @animals.route('/animals/<int:animal_id>', methods=['GET', 'DELETE', 'PUT'])
# @token_required
# def get_one_animal(_center_id, animal_id):
#     if request.method == 'PUT':
#         request_data = request.get_json()
#         try:
#             is_center_id_valid(_center_id, animal_id)
#         except IncorrectCredentialsException:
#             msg = 'you\'re trying to update an animal which isn\'t related to your id'
#             return jsonify({"error": msg}), 409
#         new_animal_data = (animal_id, _center_id, request_data['name'], request_data['age'], request_data['specie'])
#         try:
#             update_animal(new_animal_data)
#         except:
#             msg = 'You\'re trying to update an animal of not existing specie'
#             return jsonify({"error": msg}), 409
#         log_put_delete_requests(request.method, request.url, _center_id, request.path)
#         msg = "an animal updated successfully"
#         return jsonify({"success": msg}), 200
#
#     elif request.method == 'DELETE':
#         try:
#             is_center_id_valid(_center_id, animal_id)
#         except IncorrectCredentialsException:
#             msg = 'you\'re trying to delete an animal which isn\'t related to your id'
#             return jsonify({"error": msg}), 409
#         except AnimalNotFoundException:
#             msg = 'you\'re trying to delete an animal which doesn\'t exist'
#             return jsonify({"error": msg}), 404
#         log_put_delete_requests(request.method, request.url, _center_id, request.path)
#
#         delete_animal(animal_id)
#
#         msg = "an animal deleted successfully"
#         return jsonify({"success": msg}), 204
#
#     try:
#         is_center_id_valid(_center_id, animal_id)
#     except IncorrectCredentialsException:
#         msg = 'you\'re trying to view the animal which isn\'t related to your id'
#         return jsonify({"error": msg}), 409
#     except AnimalNotFoundException:
#         msg = 'you\'re looking for an animal which doesn\'t exist'
#         return jsonify({"error": msg}), 404
#     return jsonify(get_animal(animal_id)), 200
