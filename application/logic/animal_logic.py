from application import db
from application.models.animal import Animal, make_json
from application.models.center import Center
from application.exceptions.validation_exceptions import IncorrectCredentialsException, AnimalExistsException, \
    SpecieDoesNotExistException, AnimalNotFoundException
from application.models.specie import Specie


def get_all_animals():
    return [make_json(animal) for animal in Animal.query.all()]


def delete_animal(_animal_id):
    animal = Animal.query.get(_animal_id)
    db.session.delete(animal)
    db.session.commit()


def get_animal(_animal_id):
    animal = Animal.query.get(_animal_id)
    if animal is None:
        raise AnimalNotFoundException
    return make_json(animal)


def add_animal(_center_id, _name, _age, _specie):
    is_there_exact_animal(_center_id, _name, _age, _specie)
    is_specie_exist(_specie)
    r_center = Center.query.get(_center_id)
    new_animal = Animal(center=r_center, name=_name, age=_age, specie=_specie)
    db.session.add(new_animal)
    db.session.commit()
    return make_json(new_animal)


def is_specie_exist(_specie):
    if Specie.query.filter_by(name=_specie).one_or_none() is None:
        raise SpecieDoesNotExistException


def update_animal(animal_data):
    existed_animal = Animal.query.get(animal_data[0])
    existed_animal.center_id = animal_data[1]
    existed_animal.name = animal_data[2]
    existed_animal.age = animal_data[3]
    existed_animal.specie = animal_data[4]
    db.session.add(existed_animal)
    db.session.commit()


def get_all_animals_for_center(_center_id):
    return [make_json(animal) for animal in Animal.query.filter(Animal.center_id == _center_id)]


def is_center_id_valid(_animal_id, _center_id):
    animal = get_animal(_animal_id)
    if animal['center_id'] == _center_id:
        raise IncorrectCredentialsException


def is_there_exact_animal(_center_id, _name, _age, _specie):
    existing_animal = Animal.query.filter(Animal.center_id == _center_id) \
        .filter(Animal.name == _name).filter(Animal.age == _age) \
        .filter(Animal.specie == _specie).one_or_none()
    if existing_animal is not None:
        raise AnimalExistsException
