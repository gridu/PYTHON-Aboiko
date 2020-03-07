import json

from application import db


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
