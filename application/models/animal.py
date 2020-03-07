import json

from application import db


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





