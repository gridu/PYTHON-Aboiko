import json

from application import db
from .center import Center
from .exceptions.validation_exceptions import AnimalExistsException, AnimalNotFoundException, \
    IncorrectCredentialsException, SpecieDoesNotExistException
from .specie import Specie


def make_json(self):
    return {
        'id': self.id,
        'center_id': self.center_id,
        'name': self.name,
        'age': self.age,
        'specie': self.specie
    }


class Animal(db.Model):
    __tablename__ = "animal"
    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, db.ForeignKey("center.id"))
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    specie = db.Column(db.String, nullable=True)

    def __repr__(self):
        animal_object = {
            'center_id': self.center_id,
            'name': self.name,
            'age': self.age,
            'specie': self.specie,
            'id': self.animal_id
        }
        return json.dumps(animal_object)


# def count_animals():
#     return db.session.query(Animal).count()


def get_all_animals():
    return [make_json(animal) for animal in Animal.query.all()]


def delete_animal(_animal_id):
    # animal = Animal.query.filter_by(id=_animal_id).first()
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


def is_specie_exist(_specie):
    if Specie.query.filter_by(name=_specie).one_or_none() is None:
        raise SpecieDoesNotExistException


def update_animal(_animal_id, animal):
    existed_animal = Animal.query.get(_animal_id)
    existed_animal.name = animal.name
    existed_animal.age = animal.age
    existed_animal.specie = animal.specie
    existed_animal.center_id = animal.center_id
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
