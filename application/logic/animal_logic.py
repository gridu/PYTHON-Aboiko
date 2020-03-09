import json

from flask import make_response, jsonify, Response

from application import db
from application.models.animal import Animal, make_json
from application.models.center import Center
from application.validations.animal_specie_validations import is_there_exact_animal, is_specie_exist, is_center_id_valid


def delete_animal(_center_id, _animal_id):
    """
    This function deletes a animal from the animal structure

    :param _animal_id:
    :param animal_id:     Id of the animal to delete
    :return:            200 on successful delete, 404 if not found
    """
    animal = Animal.query.get(_animal_id)
    if animal is None:
        msg = 'you\'re trying to delete an animal which doesn\'t exist'
        return make_response(jsonify({"error": msg}), 404)
    if not is_center_id_valid(_center_id, animal):
        msg = 'you\'re trying to delete an animal which isn\'t related to your id'
        return make_response(jsonify({"error": msg}), 409)
    db.session.delete(animal)
    db.session.commit()
    msg = "an animal deleted successfully"
    return make_response(jsonify({"success": msg}), 200)


def get_animal(_center_id, _animal_id):
    """
    This function responds to a request for /animals/{animal_id}
    with one matching animal if this animal is related
    to the center_id which makes a request

    :param _animal_id:         Id of the animal
    :return:                json string of animal contents
    """
    animal = Animal.query.get(_animal_id)
    if animal is None:
        msg = 'you\'re looking for an animal which doesn\'t exist'
        return make_response(jsonify({"error": msg}), 404)
    if not is_center_id_valid(_center_id, animal):
        msg = 'you\'re trying to view the animal which isn\'t related to your id'
        return make_response(jsonify({"error": msg}), 409)

    return make_response(make_json(animal), 200)


def add_animal(_center_id, _name, _age, _specie):
    """
    This function creates a new animal related to the passed in center id.

    :param _age:            age of the animal from request (integer)
    :param _name:           name of the animal from request (integer)
    :param _center_id:      age of the animal from request (integer)id of a center
                            which makes a request
    :param _specie:         name of the specie from request (string)
    :return:                The JSON containing the animal data
    """
    if is_there_exact_animal(_center_id, _name, _age, _specie):
        msg = 'That animal already exists'
        return make_response(jsonify({"error": msg}), 409)
    if not is_specie_exist(_specie):
        msg = 'You\'re trying to assign an animal to not existing specie'
        return make_response(jsonify({"error": msg}), 409)
    r_center = Center.query.get(_center_id)
    new_animal = Animal(center=r_center, name=_name, age=_age, specie=_specie)
    db.session.add(new_animal)
    db.session.commit()
    animal_id = new_animal.id
    response = Response(
        response=json.dumps(make_json(new_animal)),
        status=201,
        mimetype='application/json'
    )
    response.headers['Location'] = "/animals/{0}".format(str(animal_id))
    return response


def update_animal(animal_id, animal_data):
    animal = Animal.query.get(animal_id)
    if animal is None:
        msg = 'you\'re trying to update an animal which doesn\'t exist'
        return make_response(jsonify({"error": msg}), 404)
    if not is_center_id_valid(animal_data[1], animal):
        msg = 'you\'re trying to update an animal which isn\'t related to your id'
        return make_response(jsonify({"error": msg}), 409)
    if not is_specie_exist(animal_data[4]):
        msg = 'You\'re trying to update an animal of not existing specie'
        return make_response(jsonify({"error": msg}), 409)
    existed_animal = Animal.query.get(animal_data[0])
    existed_animal.center_id = animal_data[1]
    existed_animal.name = animal_data[2]
    existed_animal.age = animal_data[3]
    existed_animal.specie = animal_data[4]
    db.session.add(existed_animal)
    db.session.commit()
    msg = "an animal updated successfully"
    return make_response(jsonify({"success": msg}), 200)


def get_all_animals_for_center(_center_id):
    return [make_json(animal) for animal in Animal.query.filter(Animal.center_id == _center_id)]
