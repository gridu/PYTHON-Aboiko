import json
from flask import jsonify
from config import *


def add_spicie(_name, _price, _description):
    new_specie = Specie(name=_name, price=_price, description=_description)
    db.session.add(new_specie)
    db.session.commit()


def get_specie(_spicie_id):
    return Specie.query.filter_by(spicie_id=_spicie_id).first()

def make_json(self):
    return {'spicie_id': self.spicie_id, 'name': self.name, 'price': self.price, 'description': self.description}

def get_all_species():
    return [make_json(specie) for specie in Specie.query.all()]


class Specie(db.Model):
    __tablename__ = "specie"
    spicie_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)

    def __repr__(self):
        spicie_object = {
            'spicie_id': self.spicie_id,
            'name': self.name,
            'price': self.price,
            'description': self.description,

        }
        return json.dumps(spicie_object)
