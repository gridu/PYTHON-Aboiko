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


def get_all_animals():
    return [make_json(animal) for animal in Animal.query.all()]


def delete_animal(_animal_id):
    animal = Animal.query.filter_by(id=_animal_id).first()
    db.session.delete(animal)
    db.session.commit()


def get_animal(_animal_id):
    return make_json(Animal.query.filter_by(id=_animal_id).first())


def add_animal(_center_id, _name, _age, _specie):
    r_center = Center.query.filter(Center.id == _center_id).one_or_none()
    new_animal = Animal(center=r_center, name=_name, age=_age, specie=_specie)

    db.session.add(new_animal)
    db.session.commit()


def update_animal(_animal_id, animal):
    existed_animal = Animal.query.filter_by(id=_animal_id).first()
    existed_animal.name = animal.name
    existed_animal.age = animal.age
    existed_animal.spicie = animal.spicie
    existed_animal.center_id = animal.center_id
    db.session.add(existed_animal)
    db.session.commit()
