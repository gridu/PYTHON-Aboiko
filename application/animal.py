import json
from application import db
from .center import Center


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

    # def __init__(self, _center_id, _name, _age, _specie):
    #     self.center_id = _center_id
    #     self.name = _name
    #     self.age = _age
    #     self.specie = _specie
    #
    # def __init__(self, _name, _age, _specie):
    #     self.name = _name
    #     self.age = _age
    #     self.specie = _specie


def get_all_animals():
    return [make_json(animal) for animal in Animal.query.all()]


def delete_animal(_animal_id):
    # animal = Animal.query.filter_by(id=_animal_id).first()
    animal = Animal.query.get(_animal_id)
    db.session.delete(animal)
    db.session.commit()


def get_animal(_animal_id):
    # return make_json(Animal.query.filter_by(id=_animal_id).first())
    return make_json(Animal.query.get(_animal_id))


def add_animal(_center_id, _name, _age, _specie):
    # r_center = Center.query.filter(Center.id == _center_id).one_or_none()
    r_center = Center.query.get(_center_id)
    new_animal = Animal(center=r_center, name=_name, age=_age, specie=_specie)

    db.session.add(new_animal)
    db.session.commit()


def update_animal(_animal_id, animal):
    # existed_animal = Animal.query.filter_by(id=_animal_id).first()
    existed_animal = Animal.query.get(_animal_id)
    existed_animal.name = animal.name
    existed_animal.age = animal.age
    existed_animal.specie = animal.specie
    existed_animal.center_id = animal.center_id
    db.session.add(existed_animal)
    db.session.commit()


def is_center_id_valid(_animal_id, _center_id):
    animal = get_animal(_animal_id)
    return animal['center_id'] == _center_id


def get_all_animals_for_center(_center_id):
    return [make_json(animal) for animal in Animal.query.filter(Animal.center_id==_center_id)]
