import json
from flask import jsonify

from . import db


def add_specie(_name, _price, _description):
    new_specie = Specie(name=_name, price=_price, description=_description)
    db.session.add(new_specie)
    db.session.commit()


def get_specie(_specie_id):
    # return Specie.make_json(Specie.query.filter_by(id=_specie_id).first())
    return Specie.make_json(Specie.query.get(_specie_id))


def get_all_species():
    return [Specie.make_json(specie) for specie in Specie.query.all()]


class Specie(db.Model):
    __tablename__ = "specie"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)

    def __repr__(self):
        specie_object = {
            'specie_id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,

        }
        return json.dumps(specie_object)

    def make_json(self):
        return {'specie_id': self.id,
                'name': self.name,
                'price': self.price,
                'description': self.description}
